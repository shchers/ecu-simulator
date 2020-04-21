#!/usr/bin/env python3

import tkinter as tk

# PIDs dictionary. As a reference used Wiki - https://en.wikipedia.org/wiki/OBD-II_PIDs
Pids = {
	1 : {
		0x00 : {
			"name" : "PIDs supported [01 - 20]",	# PID name
			"len" : 4,								# Response length
			"is-property" : True,					# Not a value, but changable param
			"static" : True,						# Static param
			"min" : 0,								# Min param value, not used if "is-property"
			"max" : 0,								# Max param value, not used if "is-property"
			"units" : "n/a",						# Value units
		},
		0x01 : {
			"name" : "Monitor status since DTCs cleared",
			"len" : 4,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "n/a",
		},
		0x02 : {
			"name" : "Freeze DTC",
			"len" : 2,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "n/a",
		},
		0x03 : {
			"name" : "Fuel system status",
			"len" : 2,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "n/a",
		},
		0x04 : {
			"name" : "Calculated engine load",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : 0,
			"max" : 100,
			"units" : "%",
		},
		0x05 : {
			"name" : "Engine coolant temperature",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : -40,
			"max" : 215,
			"units" : "°C",
		},
		0x06 : {
			"name" : "Short term fuel trim-Bank 1",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : -100,
			"max" : 99.2,
			"units" : "%",
		},
		0x07 : {
			"name" : "Long term fuel trim-Bank 1",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : -100,
			"max" : 99.2,
			"units" : "%",
		},
		0x08 : {
			"name" : "Short term fuel trim-Bank 2",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : -100,
			"max" : 99.2,
			"units" : "%",
		},
		0x09 : {
			"name" : "Long term fuel trim-Bank 2",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : -100,
			"max" : 99.2,
			"units" : "%",
		},
		0x0a : {
			"name" : "Fuel pressure",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : 0,
			"max" : 765,
			"units" : "kPa",
		},
		0x0b : {
			"name" : "Intake manifold absolute pressure",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : 0,
			"max" : 255,
			"units" : "kPa",
		},
		0x0c : {
			"name" : "Engine RPM",
			"len" : 2,
			"is-property" : False,
			"static" : False,
			"min" : 0,
			"max" : 16383.75,
			"units" : "rpm",
		},
		0x0d : {
			"name" : "Vehicle speed",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : 0,
			"max" : 255,
			"units" : "km/h",
		},
		0x0e : {
			"name" : "Timing advance",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : -64,
			"max" : 63.5,
			"units" : "° before TDC",
		},
		0x0f : {
			"name" : "Intake air temperature",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : -40,
			"max" : 215,
			"units" : "°C",
		},
		0x10 : {
			"name" : "MAF air flow rate",
			"len" : 2,
			"is-property" : False,
			"static" : False,
			"min" : 0,
			"max" : 655.35,
			"units" : "grams/sec",
		},
		0x11 : {
			"name" : "Throttle position",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : 0,
			"max" : 100,
			"units" : "%",
		},
		0x12 : {
			"name" : "Commanded secondary air status",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x13 : {
			"name" : "Oxygen sensors present (in 2 banks)",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x14 : {
			"name" : "Oxygen Sensor 1",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x15 : {
			"name" : "Oxygen Sensor 2",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x16 : {
			"name" : "Oxygen Sensor 3",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : ""
		},
		0x17 : {
			"name" : "Oxygen Sensor 4",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x18 : {
			"name" : "Oxygen Sensor 5",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x19 : {
			"name" : "Oxygen Sensor 6",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x1a : {
			"name" : "Oxygen Sensor 7",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x1b : {
			"name" : "Oxygen Sensor 8",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x1c : {
			"name" : "OBD standards this vehicle conforms to",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x1d : {
			"name" : "Oxygen sensors present (in 4 banks)",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x1e : {
			"name" : "Auxiliary input status",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
		0x1f : {
			"name" : "Run time since engine start",
			"len" : 1,
			"is-property" : False,
			"static" : False,
			"min" : 0,
			"max" : 65535,
			"units" : "seconds",
		},
		0x20 : {
			"name" : "PIDs supported [21 - 40]",
			"len" : 1,
			"is-property" : True,
			"static" : False,
			"min" : 0,
			"max" : 0,
			"units" : "",
		},
	}
}


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.minsize(width=400, height=800)
		tk.Grid.rowconfigure(master, 0, weight=1)
		tk.Grid.columnconfigure(master, 0, weight=1)

		# Variables
		self.var = [tk.BooleanVar() for i in range(32)]

		self.create_controls()

	def create_controls(self):
		frame=tk.Frame(self.master)
		frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

		row_id = 0

		for i in range(32):
			try:
				pid_name = 'PID ${:02X} - {:s}'.format(i + 1, Pids[1][i + 1]["name"])
			except:
				pid_name = 'PID ${:02X}'.format(i + 1)

			cb = tk.Checkbutton(frame, text=pid_name,
				variable=self.var[i], command=self.on_cb_changed)
			cb.grid(row=row_id, column=3, sticky=tk.W)
			row_id += 1

		self.pids_entry = tk.Entry(frame, state="readonly")
		self.pids_entry.grid(row=row_id, column=3, sticky=tk.W+tk.E)

	def on_cb_changed(self):
		val = 0
		for i in range(32):
			if self.var[i].get():
				val |= (1 << (7-(i % 8))) << (int(i/8) * 8)

		a = val & 0xff
		b = (val >> 8) & 0xff
		c = (val >> 16) & 0xff
		d = (val >> 24) & 0xff

		print('0x{:02X} 0x{:02X} 0x{:02X} 0x{:02X}'.format(a, b, c, d))

		self.pids_entry['state'] = 'normal'
		self.pids_entry.delete(0, tk.END)
		self.pids_entry.insert(0, '0x{:02X} 0x{:02X} 0x{:02X} 0x{:02X}'.format(a, b, c, d))
		self.pids_entry['state'] = 'readonly'

if __name__ == "__main__":
	window = tk.Tk()
	window.title("PIDs caps")
	app = Application(master=window)
	app.mainloop()
