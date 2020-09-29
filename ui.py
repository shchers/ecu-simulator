#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog, messagebox
import glob
import os
import getopt
import sys
from random import randint
from datetime import datetime
import threading
import logging as log

import can
from can.bus import BusState

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.minsize(width=800, height=600)
		master.protocol("WM_DELETE_WINDOW", self.close_app)
		tk.Grid.rowconfigure(master, 0, weight=1)
		tk.Grid.columnconfigure(master, 0, weight=1)

		# CAN bus
		self.event = threading.Event()
		self.bus = None
		self.can_is_started = False

		# Ceate variables
		self.can_device_var = tk.StringVar()
		self.speed_var = tk.IntVar()
		self.speed_var_auto = tk.BooleanVar()
		self.speed_var_min = tk.IntVar()
		self.speed_var_max = tk.IntVar()
		self.rpm_var = tk.DoubleVar()
		self.rpm_var_auto = tk.BooleanVar()
		self.rpm_var_min = tk.DoubleVar()
		self.rpm_var_max = tk.DoubleVar()

		self.create_controls()

	def close_app(self):
		if self.can_is_started:
			self.can_disconnect()

		self.master.destroy()

	def get_can_devices(self):
		# XXX: not really good to limit the list only to can
		# TODO: add support for different CAN interfaces
		devices = glob.glob('/sys/class/net/can*')
		for i in range(len(devices)):
			devices[i] = os.path.basename(devices[i])
		return devices

	def create_controls(self):
		frame=tk.Frame(self.master)
		frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

		frame.columnconfigure(1, weight=1)
		frame.columnconfigure(4, weight=1)
		frame.columnconfigure(5, weight=1)


		# Row index
		row_id = 0

		can_frame = tk.LabelFrame(frame, text="Interface")
		can_frame.grid(row=row_id, column=0, padx=(10, 10), sticky=tk.W+tk.W+tk.N+tk.S)

		devices = self.get_can_devices()
		if len(devices) > 0:
			self.can_device_var.set(devices[0])
		else:
			devices.append('')

		self.can_options = tk.OptionMenu(can_frame, self.can_device_var, *devices)
		self.can_options.grid(row=0, column=0, pady=(5, 10), sticky=tk.W+tk.E)

		btn_refresh = tk.Button(can_frame, text="R", command=self.refresh_list)
		btn_refresh.grid(row=0, column=1, pady=(5, 10), sticky=tk.E)

		self.connect = tk.Button(can_frame, text="Connect", command=self.can_connect)
		self.connect.grid(row=1, column=0, sticky=tk.W+tk.E)

		self.disconnect = tk.Button(can_frame, text="Disconnect", state="disabled", command=self.can_disconnect)
		self.disconnect.grid(row=2, column=0, sticky=tk.W+tk.E)

		# New row - Speed entry
		row_id += 1

		self.lbl_speed = tk.Label(frame, text="Speed, km/h")
		self.lbl_speed.grid(row=row_id, column=0, padx=(10, 10), sticky=tk.W)

		self.sc_speed = tk.Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL,
			variable=self.speed_var)
		self.sc_speed.grid(row=row_id, column=1, padx=(5, 5), sticky=tk.W+tk.E)

		self.cb_speed_auto = tk.Checkbutton(frame, text="Auto mode",
			variable=self.speed_var_auto, command=self.on_cb_speed_auto)
		self.cb_speed_auto.grid(row=row_id, column=3)

		self.sc_speed_min = tk.Scale(frame, from_=0, to=254, orient=tk.HORIZONTAL, label="Min",
			state="disabled", variable=self.speed_var_min, command=self.on_sc_speed)
		self.sc_speed_min.grid(row=row_id, column=4, padx=(5, 5), sticky=tk.W+tk.E)

		self.sc_speed_max = tk.Scale(frame, from_=1, to=255, orient=tk.HORIZONTAL, label="Max",
			state="disabled", variable=self.speed_var_max, command=self.on_sc_speed)
		self.sc_speed_max.grid(row=row_id, column=5, padx=(5, 10), sticky=tk.W+tk.E)

		# New row - RPM entry
		row_id += 1

		self.lbl_rpm = tk.Label(frame, text="RPM, km/h")
		self.lbl_rpm.grid(row=row_id, column=0, padx=(10, 10), sticky=tk.W)

		self.sc_rpm = tk.Scale(frame, from_=0, to=16383.75, orient=tk.HORIZONTAL,
			resolution=0.25, variable=self.rpm_var)
		self.sc_rpm.grid(row=row_id, column=1, padx=(5, 5), sticky=tk.W+tk.E)

		self.cb_rpm_auto = tk.Checkbutton(frame, text="Auto mode",
			variable=self.rpm_var_auto, command=self.on_cb_rpm_auto)
		self.cb_rpm_auto.grid(row=row_id, column=3)

		self.sc_rpm_min = tk.Scale(frame, from_=0, to=16383.75, orient=tk.HORIZONTAL, label="Min",
			resolution=0.25, state="disabled", variable=self.rpm_var_min, command=self.on_sc_rpm)
		self.sc_rpm_min.grid(row=row_id, column=4, padx=(5, 5), sticky=tk.W+tk.E)

		self.sc_rpm_max = tk.Scale(frame, from_=1, to=16383.75, orient=tk.HORIZONTAL, label="Max",
			resolution=0.25, state="disabled", variable=self.rpm_var_max, command=self.on_sc_rpm)
		self.sc_rpm_max.grid(row=row_id, column=5, padx=(5, 10), sticky=tk.W+tk.E)

		# New row
		row_id += 1

		tk.Grid.rowconfigure(frame, row_id, weight=1)

		log_frame = tk.Frame(frame)
		log_frame.grid(row=row_id, column=0, columnspan=6, padx=(10, 10), pady=(10, 10), sticky=tk.W+tk.E+tk.N+tk.S)
		log_frame.columnconfigure(0, weight=1)
		log_frame.rowconfigure(0, weight=1)

		scrollbar = tk.Scrollbar(log_frame)
		scrollbar.grid(row=0, column=1, sticky=tk.E+tk.N+tk.S)

		self.logbox = tk.Text(log_frame, background="black", foreground="medium spring green", font="Mono 10",
			yscrollcommand=scrollbar.set)
		self.logbox.configure(state='normal')
		self.logbox.insert(tk.END, "Select interface and press 'Connect' button.\n")
		self.logbox.configure(state='disabled')
		self.logbox.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

		scrollbar.config(command=self.logbox.yview)

		# New row
		row_id += 1

		buttons_frame = tk.Frame(frame)
		buttons_frame.grid(row=row_id, column=0, columnspan=6, sticky=tk.E+tk.S)

		btn_clearlog = tk.Button(buttons_frame, text="Clear log", command=self.clear_log)
		btn_clearlog.grid(row=row_id, column=0, padx=(10, 5), pady=(10, 10))

		btn_savelog = tk.Button(buttons_frame, text="Save log", command=self.save_log)
		btn_savelog.grid(row=row_id, column=1, padx=(10, 5), pady=(10, 10))

		btn_quit = tk.Button(buttons_frame, text="Quit", command=self.close_app)
		btn_quit.grid(row=row_id, column=2, padx=(5, 10), pady=(10, 10))

	def refresh_list(self):
		# Get list of CAN devices
		devices = self.get_can_devices()

		# Reset menu
		menu = self.can_options['menu']
		menu.delete(0, tk.END)
		self.can_device_var.set('')

		# Load list of devices to menu
		for device in devices:
			menu.add_command(label=device,
							 command=lambda value=device:
							 self.om_variable.set(value))

		# Set the first device in the list as a default
		if len(devices) > 0:
			self.can_device_var.set(devices[0])

	def can_disconnect(self):
		self.can_is_started = False
		self.bus.shutdown()
		self.h_receiver.join(timeout=90)
		if self.h_receiver.is_alive():
			self.add_log("Error: CAN bus thread is not stopped!")

		self.can_options['state'] = 'normal'
		self.connect['state'] = 'normal'
		self.disconnect['state'] = 'disabled'

		self.event.clear()
		self.add_log('Bus {:s} is disconnected'.format(self.can_device_var.get()))

	def can_connect(self):
		if self.can_device_var.get() == '':
			messagebox.showwarning(message="CAN interface is not available or selected")
			return

		self.bus = can.interface.Bus(bustype='socketcan', channel=self.can_device_var.get())
		if self.bus is None:
			self.add_log('Bus {:s} cannot be connected'.format(self.can_device_var.get()))
			return

		self.h_receiver = threading.Thread(target=self.receive_all)
		self.h_receiver.start()

		self.can_is_started = True
		self.disconnect['state'] = 'normal'
		self.connect['state'] = 'disabled'
		self.can_options['state'] = 'disabled'

		self.event.set()
		self.add_log('Bus {:s} is connected'.format(self.can_device_var.get()))

	def add_log(self, message):
		self.logbox.configure(state='normal')
		# Add timestamp to message
		mpt = '{:%Y.%m.%d-%H:%M:%S.%f}: {:s}\n'.format(datetime.utcnow(), message)
		self.logbox.insert(tk.END, mpt)
		self.logbox.configure(state='disabled')
		self.logbox.see(tk.END)

	def clear_log(self):
		self.logbox.configure(state='normal')
		self.logbox.delete(1.0, tk.END)
		self.logbox.configure(state='disabled')

	def save_log(self):
		files = [
			('Logs', '*.log'),
			('All Files', "*.*"),
			('Text files', '*.txt')]
		file_handler = filedialog.asksaveasfile(title = "Save log", defaultextension=".log", filetypes=files)
		if file_handler is None:
			# Looks like "Cancel" button is pressed
			return

		print(file_handler)
		file_handler.write(str(self.logbox.get(1.0, tk.END)))
		file_handler.close()

	def on_sc_speed(self, val):
		if self.speed_var_min.get() > self.speed_var_max.get():
			self.speed_var_max.set(self.speed_var_min.get() + 1)

	def on_cb_speed_auto(self):
		if self.speed_var_auto.get() != True:
			self.sc_speed_min['state'] = "disabled"
			self.sc_speed_max['state'] = "disabled"
			self.sc_speed['state'] = "normal"
		else:
			self.sc_speed_min['state'] = "normal"
			self.sc_speed_max['state'] = "normal"
			self.sc_speed['state'] = "disabled"
		pass

	def on_sc_rpm(self, val):
		if self.rpm_var_min.get() > self.rpm_var_max.get():
			self.rpm_var_max.set(self.rpm_var_min.get() + 1)

	def on_cb_rpm_auto(self):
		if self.rpm_var_auto.get() != True:
			self.sc_rpm_min['state'] = "disabled"
			self.sc_rpm_max['state'] = "disabled"
			self.sc_rpm['state'] = "normal"
		else:
			self.sc_rpm_min['state'] = "normal"
			self.sc_rpm_max['state'] = "normal"
			self.sc_rpm['state'] = "disabled"
		pass

	def service1(self, msg):
		if msg.data[2] == 0x00:
			log.debug(">> Caps")
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x06, 0x41, 0x00, 0x18, 0x3B, 0x80, 0x00],
			  is_extended_id=False)
			self.bus.send(msg)
		elif msg.data[2] == 0x04:
			log.debug(">> Calculated engine load")
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x03, 0x41, 0x04, 0x20],
			  is_extended_id=False)
			self.bus.send(msg)
		elif msg.data[2] == 0x05:
			log.debug(">> Engine coolant temperature")
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x03, 0x41, 0x05, randint(88 + 40, 95 + 40)],
			  is_extended_id=False)
			self.bus.send(msg)
		elif msg.data[2] == 0x0B:
			log.debug(">> Intake manifold absolute pressure")
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x04, 0x41, 0x0B, randint(10, 40)],
			  is_extended_id=False)
			self.bus.send(msg)
		elif msg.data[2] == 0x0C:
			log.debug(">> RPM")

			if self.rpm_var_auto.get():
				val = randint(self.rpm_var_min.get(), self.rpm_var_max.get())
			else:
				val = self.rpm_var.get()

			val *= 4
			valA = int(val / 256)
			valB = int(val - valA*256)

			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x04, 0x41, 0x0C, valA, valB],
			  is_extended_id=False)
			self.bus.send(msg)
		elif msg.data[2] == 0x0D:
			log.debug(">> Speed")

			if self.speed_var_auto.get():
				val = randint(self.speed_var_min.get(), self.speed_var_max.get())
			else:
				val = self.speed_var.get()

			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x03, 0x41, 0x0D, val],
			  is_extended_id=False)
			self.bus.send(msg)
		elif msg.data[2] == 0x0F:
			log.debug(">> Intake air temperature")
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x03, 0x41, 0x0F, randint(60, 64)],
			  is_extended_id=False)
			self.bus.send(msg)
		elif msg.data[2] == 0x10:
			log.debug(">> MAF air flow rate")
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x04, 0x41, 0x10, 0x00, 0xFA],
			  is_extended_id=False)
			self.bus.send(msg)
		elif msg.data[2] == 0x11:
			log.debug(">> Throttle position")
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x03, 0x41, 0x11, randint(20, 60)],
			  is_extended_id=False)
			self.bus.send(msg)
		elif msg.data[2] == 0x33:
			log.debug(">> Absolute Barometric Pressure")
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x03, 0x41, 0x33, randint(20, 60)],
			  is_extended_id=False)
			self.bus.send(msg)
		else:
			self.add_log('Service 1, unknown PID=0x{:02x}'.format(msg.data[2]))

	def service9(self, msg):
		if msg.data[2] == 0x02:
			log.debug(">> VIN code")
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x10, 0x14, 0x49, 0x02, 0x01, 0x33, 0x46, 0x41],
			  is_extended_id=False)
			self.bus.send(msg)
			#
			# XXX: Need to be designed and implemented correct handling for "continue" request:
			# 7E0   [8]  30 00 00 00 00 00 00 00
			#
			# Right now we just sending all VIN code, i.e. without hand-shaking - that is not good
			#
			# Also, here hardcoded VIN of some unknown Ford and it need to be replaced with editable entry
			#
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x21, 0x44, 0x50, 0x34, 0x46, 0x4A, 0x32, 0x42],
			  is_extended_id=False)
			self.bus.send(msg)
			msg = can.Message(arbitration_id=0x7e8,
			  data=[0x22, 0x4D, 0x31, 0x31, 0x33, 0x39, 0x31, 0x33],
			  is_extended_id=False)
			self.bus.send(msg)
		else:
			self.add_log('Service 9, unknown PID=0x{:02x}'.format(msg.data[2]))

	def receive_all(self):
		self.event.wait()

		while self.can_is_started:
			msg = self.bus.recv(1)
			# Just skip 'bad' messages
			if msg is None:
				continue

			if msg.arbitration_id != 0x7df:
				self.add_log('Unknown Id 0x{:03x}'.format(msg.arbitration_id))
				continue

			if msg.data[1] == 0x01:
				self.service1(msg)
			elif msg.data[1] == 0x09:
				self.service9(msg)
			else:
				self.add_log('Service {:d} is not supported'.format(msg.data[1]))

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "l:v", ["loglevel="])
	except getopt.GetoptError as err:
		# print help information and exit:
		print(err)  # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	loglevel = "INFO"

	for o, a in opts:
		if o == "-v":
			loglevel = "DEBUG"
		elif o in ("-l", "--loglevel"):
			loglevel = a
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		else:
			assert False, "unhandled option"

	numeric_level = getattr(log, loglevel.upper(), None)
	if not isinstance(numeric_level, int):
		raise ValueError('Invalid log level: %s' % loglevel)
	log.basicConfig(level=numeric_level)

	window = tk.Tk()
	window.title("ECU Simulator")
	app = Application(master=window)
	app.mainloop()
