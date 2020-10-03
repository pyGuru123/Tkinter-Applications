# Trigonometric ratios graph visualizer

# Importing libraries ------------------------------------------------------

# pip install numpy
# pip install matplotlib

from plot import get_plot

import tkinter as tk
from tkinter import PhotoImage

import numpy as np
import matplotlib
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")

# Application Class --------------------------------------------------------

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		
		self.v1 = tk.StringVar()
		self.v2 = tk.StringVar()
		self.initialized = True

		self.draw_frames()
		self.draw_widgets()
		self.draw_graph_frame()

	def draw_frames(self):
		self.head = tk.LabelFrame(self, text='', 
					font=("times new roman",15,"bold"),
					bg="white",bd=1,relief=tk.GROOVE)
		self.head.config(width=780,height=100)
		self.head.grid(row=0, column=0, columnspan=5)

		self.ratios = tk.LabelFrame(self, text='', 
					font=("times new roman",15,"bold"),
					bg="white",bd=0,relief=tk.GROOVE)
		self.ratios.config(width=200,height=410)
		self.ratios.grid(row=1, column=0, pady=10)

	def draw_widgets(self):
		self.title = tk.Label(self.head)
		self.title['text'] = 'Graph Visulaizer'
		self.title.config(height=2, width=108)
		self.title.grid(row=0, column=0, columnspan=8, padx=8, pady=10)

		self.label1 = tk.Label(self.head)
		self.label1['text'] = '\tMin'
		self.label1.grid(row=1, column=4, pady=8)
		self.min = tk.Entry(self.head)
		self.min['textvariable'] = self.v1
		self.min.grid(row=1, column=5, padx=8, pady=8)

		self.label2 = tk.Label(self.head)
		self.label2['text'] = '\tMax'
		self.label2.grid(row=1, column=6, pady=8)
		self.max = tk.Entry(self.head)
		self.max['textvariable'] = self.v2
		self.max.grid(row=1, column=7, pady=8)

		ratio_padx = 30
		ratio_pady = 15

		self.sin = self.create_button(' sin ', lambda : self.plot_ratio('sin'), 1, 0, ratio_padx, ratio_pady )
		self.cos = self.create_button(' cos ', lambda : self.plot_ratio('cos'), 2, 0, ratio_padx, ratio_pady )
		self.tan = self.create_button(' tan ', lambda : self.plot_ratio('tan'), 3, 0, ratio_padx, ratio_pady )
		self.cosec = self.create_button(' cosec ', lambda : self.plot_ratio('cosec'), 4, 0, ratio_padx, ratio_pady )
		self.sec = self.create_button(' sec ', lambda : self.plot_ratio('sec'), 5, 0, ratio_padx, ratio_pady )
		self.cot = self.create_button(' cot ', lambda : self.plot_ratio('cot'), 6, 0, ratio_padx, ratio_pady )

	def draw_graph_frame(self):
		self.graph = tk.LabelFrame(self, text='', 
					font=("times new roman",16,"bold"),
					bg="white",bd=1,relief=tk.GROOVE)
		self.graph.config(width=580,height=410)
		self.graph.grid(row=1, column=1, pady=10) 

		if self.initialized:
			self.text = tk.Text(self.graph)
			self.text.grid(row=0, column=0)
			self.intro = tk.PhotoImage(file='files/intro.png')
			self.text.image_create(tk.END, image = self.intro)
			self.initialized = False
		else:
			self.figure = Figure(figsize=(6, 4), dpi=100)
			self.canvas = FigureCanvasTkAgg(self.figure, self.graph)
			self.canvas.get_tk_widget().grid(row=0, column=0)

	def create_button(self, text, command, r, c, x, y):
		self.button = tk.Button(self.ratios, bg='green', fg='white', font=10)
		self.button['text'] = text 
		self.button.config(width=13)
		self.button['command'] = command
		self.button.grid(row=r, column=c, padx=x, pady=y)

	def plot_ratio(self, ratio):
		if self.min.get() == '' or self.max.get() == '':
			tk.messagebox.showerror('Cant plot graph', 'Give min and max values')
		else:
			m1 = float(self.min.get())
			m2 = float(self.max.get())

			self.graph.destroy()
			self.draw_graph_frame()
			self.figure = get_plot(m1, m2, ratio)
			self.canvas = FigureCanvasTkAgg(self.figure, self.graph)
			self.canvas.get_tk_widget().grid(row=0, column=0)


# Main App -------------------------------------------------------------------------

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('800x520')
	root.wm_title('Graph Visualizer')

	app = Application(master=root)
	app.mainloop()