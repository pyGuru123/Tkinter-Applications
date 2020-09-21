# Trigonometric ratios graph visualizer
# project by pyGuru
# Visit pyGuru on youtube

# Importing libraries ------------------------------------------------------

# pip install numpy
# pip install matplotlib

import tkinter as tk

import numpy as np
import matplotlib
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Defining functions---------------------------------------------------------

matplotlib.use("TkAgg")

def get_plot(m1, m2, func):
	v1 = m1 * np.pi / 180
	v2 = m2 * np.pi / 180

	figure = Figure(figsize=(6, 4), dpi=100)
	plot = figure.add_subplot(111)

	x = np.linspace(v1, v2, 1000)

	if func == 'sin':
		y = np.sin(x)
		plot.plot(x, y)
	elif func == 'cos':
		y = np.cos(x)
		plot.plot(x, y)
	elif func == 'tan':
		y = np.tan(x)
		y[:-1][np.diff(y) < 0] = np.nan
		plot.plot(x, y)
		plot.set_ylim(-10,10)
	elif func == 'cosec':
		y = 1 / np.sin(x)
		plot.plot(x, y)
		plot.set_ylim(-10,10)
	elif func == 'sec':
		y = 1 / np.cos(x)
		plot.plot(x, y)
		plot.set_ylim(-10,10)
	elif func == 'cot':
		y = 1 / np.tan(x)
		y[:-1][np.diff(y) > 0] = np.nan
		plot.plot(x, y)
		plot.set_ylim(-10,10)

	plot.set_title(f'Graph of {func}(x)')
	plot.set_xlabel(f'x values from {m1} to {m2}')
	plot.set_ylabel('y(x)')

	return figure

# Application class ------------------------------------------------------------

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.head = tk.Button(self)
		self.head['text'] = 'Graph Visulaizer'
		self.head.config(height=2, width=100)
		self.head.grid(row=0, column=0, rowspan=1, columnspan=5, padx=8, pady=10)

		self.v1 = tk.StringVar()
		self.v2 = tk.StringVar()

		self.label1 = tk.Label(self)
		self.label1['text'] = '\tMin'
		self.label1.grid(row=2, column=1, pady=8)
		self.min = tk.Entry(self)
		self.min['textvariable'] = self.v1
		self.min.grid(row=2, column=2, padx=8, pady=8)

		self.label2 = tk.Label(self)
		self.label2['text'] = '\tMax'
		self.label2.grid(row=2, column=3, pady=8)
		self.max = tk.Entry(self)
		self.max['textvariable'] = self.v2
		self.max.grid(row=2, column=4, pady=8)

		self.sin = tk.Button(self, bg='green', fg='white', font=10)
		self.sin['text'] = ' sin '
		self.sin.config(height=1, width =10)
		self.sin['command'] = self.sine
		self.sin.grid(row=3, column=0, pady=6)

		self.cos = tk.Button(self, bg='green', fg='white', font=10)
		self.cos['text'] = ' cos '
		self.cos.config(height=1, width =10)
		self.cos['command'] = self.cosine
		self.cos.grid(row=4, column=0, pady=6)

		self.tan = tk.Button(self, bg='green', fg='white', font=10)
		self.tan['text'] = ' tan '
		self.tan.config(height=1, width =10)
		self.tan['command'] = self.tangent
		self.tan.grid(row=5, column=0, pady=6)

		self.cosec = tk.Button(self, bg='green', fg='white', font=10)
		self.cosec['text'] = 'cosec'
		self.cosec.config(height=1, width =10)
		self.cosec['command'] = self.cosecant
		self.cosec.grid(row=6, column=0, pady=6)

		self.sec = tk.Button(self, bg='green', fg='white', font=10)
		self.sec['text'] = ' sec '
		self.sec.config(height=1, width =10)
		self.sec['command'] = self.secant
		self.sec.grid(row=7, column=0, pady=6)

		self.cot = tk.Button(self, bg='green', fg='white', font=10)
		self.cot['text'] = ' cot '
		self.cot.config(height=1, width =10)
		self.cot['command'] = self.cotangent
		self.cot.grid(row=8, column=0, pady=6)

		self.figure = Figure(figsize=(6, 4), dpi=100)
		self.canvas = FigureCanvasTkAgg(self.figure, self)
		self.canvas.get_tk_widget().grid(row=3, column=2, pady=6, rowspan=6, columnspan=4)


	def sine(self):
		if self.min.get() == '' or self.max.get() == '':
			tk.messagebox.showerror('Cant plot graph', 'Give min and max values')
		else:
			m1 = float(self.min.get())
			m2 = float(self.max.get())

			self.figure.clear()
			self.figure = get_plot(m1, m2, 'sin')

			self.canvas = FigureCanvasTkAgg(self.figure, self)
			self.canvas.get_tk_widget().grid(row=3, column=2, pady=8, rowspan=6, columnspan=4)

	def cosine(self):
		if self.min.get() == '' or self.max.get() == '':
			tk.messagebox.showerror('Cant plot graph', 'Give min and max values')
		else:
			m1 = float(self.min.get())
			m2 = float(self.max.get())

			self.figure.clear()
			self.figure = get_plot(m1, m2, 'cos')

			self.canvas = FigureCanvasTkAgg(self.figure, self)
			self.canvas.get_tk_widget().grid(row=3, column=2, pady=8, rowspan=6, columnspan=4)

	def tangent(self):
		if self.min.get() == '' or self.max.get() == '':
			tk.messagebox.showerror('Cant plot graph', 'Give min and max values')
		else:
			m1 = float(self.min.get())
			m2 = float(self.max.get())

			self.figure.clear()
			self.figure = get_plot(m1, m2, 'tan')

			self.canvas = FigureCanvasTkAgg(self.figure, self)
			self.canvas.get_tk_widget().grid(row=3, column=2, pady=8, rowspan=6, columnspan=4)

	def cosecant(self):
		if self.min.get() == '' or self.max.get() == '':
			tk.messagebox.showerror('Cant plot graph', 'Give min and max values')
		else:
			m1 = float(self.min.get())
			m2 = float(self.max.get())

			self.figure.clear()
			self.figure = get_plot(m1, m2, 'cosec')

			self.canvas = FigureCanvasTkAgg(self.figure, self)
			self.canvas.get_tk_widget().grid(row=3, column=2, pady=8, rowspan=6, columnspan=4)

	def secant(self):
		if self.min.get() == '' or self.max.get() == '':
			tk.messagebox.showerror('Cant plot graph', 'Give min and max values')
		else:
			m1 = float(self.min.get())
			m2 = float(self.max.get())

			self.figure.clear()
			self.figure = get_plot(m1, m2, 'sec')

			self.canvas = FigureCanvasTkAgg(self.figure, self)
			self.canvas.get_tk_widget().grid(row=3, column=2, pady=8, rowspan=6, columnspan=4)

	def cotangent(self):
		if self.min.get() == '' or self.max.get() == '':
			tk.messagebox.showerror('Cant plot graph', 'Give min and max values')
		else:
			m1 = float(self.min.get())
			m2 = float(self.max.get())

			self.figure.clear()
			self.figure = get_plot(m1, m2, 'cot')

			self.canvas = FigureCanvasTkAgg(self.figure, self)
			self.canvas.get_tk_widget().grid(row=3, column=2, pady=8, rowspan=6, columnspan=4)

# Main App -------------------------------------------------------------------------

root = tk.Tk()
root.geometry('800x520')
root.wm_title('Graph Visualizer')

app = Application(master=root)
app.mainloop()