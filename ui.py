#!/usr/bin/env python3

import tkinter as tk
from tkinter import filedialog
#import tkinter.ttk as ttk
import glob
import os

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.minsize(width=800, height=600)
		tk.Grid.rowconfigure(master, 0, weight=1)
		tk.Grid.columnconfigure(master, 0, weight=1)

		# Ceate variables
		self.can_device_var = tk.StringVar()
		self.gearbox_var = tk.IntVar()
		self.speed_var = tk.IntVar()
		self.speed_var_auto = tk.BooleanVar()
		self.rpm_var = tk.IntVar()
		self.rpm_var_auto = tk.BooleanVar()

		#self.create_widgets()
		self.create_controls()

	def create_widgets(self):
		self.hi_there = tk.Button(self)
		self.hi_there["text"] = "Hello World\n(click me)"
		self.hi_there["command"] = self.say_hi
		self.hi_there.grid(row=row_id, column=0)
		self.hi_there.pack(side="top")

		self.quit = tk.Button(self, text="QUIT", fg="red",
							  command=self.master.destroy)
		self.quit.pack(side="bottom")

	def get_can_devices(self):
		# XXX: not really good to limit the list only to can
		# TODO: add support for different CAN interfaces
		devices = glob.glob('/sys/class/net/can*')
		for i in range(len(devices)):
			devices[i] = os.path.basename(devices[i])
		return devices

	def create_controls(self):
		# Gearbox positions
		gearbox_list = {
			"Parking" : "0",
			"Revers" : "1",
			"Neutral" : "2",
			"Drive" : "3"
		}

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
		can_options = tk.OptionMenu(can_frame, self.can_device_var, *devices)
		can_options.grid(row=0, column=0, pady=(5, 10), sticky=tk.W+tk.E)

		self.connect = tk.Button(can_frame, text="Connect")
		self.connect.grid(row=1, column=0, sticky=tk.W+tk.E)

		self.disconnect = tk.Button(can_frame, text="Disconnect")
		self.disconnect.grid(row=2, column=0, sticky=tk.W+tk.E)

		gearbox_frame = tk.LabelFrame(frame, text="Gearbox")
		gearbox_frame.grid(row=row_id, column=1, padx=(5, 5), sticky=tk.W+tk.W+tk.N+tk.S)

		for (gear, val) in gearbox_list.items():
			rb_gearbox = tk.Radiobutton(gearbox_frame,
				text=gear,
				padx = 5,
				variable=self.gearbox_var,
				command=self.on_rb_gearbox,
				value=val)
			rb_gearbox.grid(row=val, column=0, sticky=tk.W)

		# New row
		row_id += 1

		self.lbl_speed = tk.Label(frame, text="Speed, km/h")
		self.lbl_speed.grid(row=row_id, column=0, padx=(10, 10), sticky=tk.W)

		self.sc_speed = tk.Scale(frame, from_=0, to=255, orient=tk.HORIZONTAL,
			command=self.on_sc_speed)
		self.sc_speed.grid(row=row_id, column=1, padx=(5, 5), sticky=tk.W+tk.E)

		self.cb_speed_auto = tk.Checkbutton(frame, text="Auto mode",
			variable=self.speed_var_auto, command=self.on_cb_speed_auto)
		self.cb_speed_auto.grid(row=row_id, column=3)

		self.sc_speed_min = tk.Scale(frame, from_=0, to=254, orient=tk.HORIZONTAL, label="Min",
			state="disabled", command=self.on_sc_speed)
		self.sc_speed_min.grid(row=row_id, column=4, padx=(5, 5), sticky=tk.W+tk.E)

		self.sc_speed_max = tk.Scale(frame, from_=1, to=255, orient=tk.HORIZONTAL, label="Max",
			state="disabled", command=self.on_sc_speed)
		self.sc_speed_max.grid(row=row_id, column=5, padx=(5, 10), sticky=tk.W+tk.E)

		# New row
		row_id += 1

		self.lbl_rpm = tk.Label(frame, text="RPM, km/h")
		self.lbl_rpm.grid(row=row_id, column=0, padx=(10, 10), sticky=tk.W)

		self.sc_rpm = tk.Scale(frame, from_=0, to=16384, orient=tk.HORIZONTAL,
			command=self.on_sc_rpm)
		self.sc_rpm.grid(row=row_id, column=1, padx=(5, 5), sticky=tk.W+tk.E)

		self.cb_rpm_auto = tk.Checkbutton(frame, text="Auto mode",
			variable=self.rpm_var_auto, command=self.on_cb_rpm_auto)
		self.cb_rpm_auto.grid(row=row_id, column=3)

		self.sc_rpm_min = tk.Scale(frame, from_=0, to=16383, orient=tk.HORIZONTAL, label="Min",
			state="disabled", command=self.on_sc_rpm)
		self.sc_rpm_min.grid(row=row_id, column=4, padx=(5, 5), sticky=tk.W+tk.E)

		self.sc_rpm_max = tk.Scale(frame, from_=1, to=16384, orient=tk.HORIZONTAL, label="Max",
			state="disabled", command=self.on_sc_rpm)
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
		self.logbox.insert(tk.END, "Select interface and press 'Connect' button.")
		self.logbox.grid(row=0, column=0, sticky=tk.W+tk.E+tk.N+tk.S)

		scrollbar.config(command=self.logbox.yview)

		# New row
		row_id += 1

		buttons_frame = tk.Frame(frame)
		buttons_frame.grid(row=row_id, column=0, columnspan=6, sticky=tk.E+tk.S)

		# TODO: implement
		btn_savelog = tk.Button(buttons_frame, text="Save log", command=self.save_log)
		btn_savelog.grid(row=row_id, column=0, padx=(10, 5), pady=(10, 10))

		btn_quit = tk.Button(buttons_frame, text="Quit", command=self.master.destroy)
		btn_quit.grid(row=row_id, column=1, padx=(5, 10), pady=(10, 10))

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
		# TODO: apply changes
		pass

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

	def on_rb_gearbox(self):
		print(self.gearbox_var.get())

	def on_sc_rpm(self, val):
		# TODO: apply changes
		pass

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

	def decrease(self):
		value = int(self.lbl_speed_val["text"])
		self.lbl_speed_val["text"] = f"{value - 1}"

	def say_hi(self):
		print("hi there, everyone!")

if __name__ == "__main__":
	window = tk.Tk()
	# width x height + x_offset + y_offset
	window.geometry("600x400+30+30")
	window.title("ECU Simulator")
	app = Application(master=window)
	app.mainloop()
