import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox

from miner import PDFMiner

cwd = os.getcwd()

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.path = None
		self.numPages = None
		self.author = None
		self.name = None

		self.draw_frames()
		self.draw_controls_frame()

	def draw_frames(self):
		self.display_frame = tk.Frame(self, width=400, height=400, bg='gray18')
		self.display_frame.grid(row=0, column=0)
		self.display_frame.grid_propagate(False)

		self.controls_frame = tk.Frame(self, width=400, height=50, bg='#252525')
		self.controls_frame.grid(row=1, column=0)
		self.controls_frame.grid_propagate(False)

	def draw_controls_frame(self):
		self.open_file_btn = ttk.Button(self.controls_frame, text='Open File', width=10, 
					command=self.open_file)
		self.open_file_btn.grid(row=0, column=0)

	def open_file(self):
		temppath = filedialog.askopenfilename(initialdir=cwd, filetypes=(("PDF","*.pdf"),))
		if temppath:
			self.path = temppath
			filename = os.path.basename(self.path)
			self.miner = PDFMiner(self.path)
			data, numpages = self.miner.get_metadata()
			if numpages:
				self.name = data.get('title', filename[:-4])
				self.author = data.get('author', None)
				self.numpages = numpages

				print(self.name, self.author, self.numPages)
			else:
				messagebox.showerror('PDF AudioBook', 'Cannot read pdf')


			

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('400x450+400+170')
	root.title('PDF AudioBook')
	root.resizable(0,0)

	app = Application(master=root)
	app.mainloop()