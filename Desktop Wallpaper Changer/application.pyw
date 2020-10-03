# Desktop Wallpaper Changer
# Random wallpapers require internet connection

import os
import ctypes
import requests
import tkinter as tk
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import messagebox

cwd = os.getcwd()

# function to check if os size is 64 bit windows or 32 bit
def is_64bit_windows():
	return ctypes.sizeof(ctypes.c_voidp) == 8


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.pack()

		self.main = True
		self.path = ''

		self.label_frame()
		self.main_frame()

	def label_frame(self):
		self.lframe = tk.LabelFrame(self, text='', 
					font=("times new roman",15,"bold"),
					bg="white", bd=1,relief=tk.GROOVE)
		self.lframe.config(width=250, height=50)
		self.lframe.grid(row=0, column=0)

		self.label = tk.Label(self.lframe, bg='white', fg='blue')
		self.label['text'] = 'Desktop Wallpaper Changer'
		self.label.configure(width=35, height=3)
		self.label.grid(row=0, column=0)

	def main_frame(self):
		self.mframe = tk.LabelFrame(self, text='', 
					font=("times new roman",15,"bold"),
					bg="white",bd=0)
		self.mframe.config(width=250, height=150)
		self.mframe.grid(row=1, column=0)

		if self.main:
			self.local = tk.Button(self.mframe, bg='green', fg='white')
			self.local['text'] = 'Choose from \n Device'
			self.local['command'] = self.choose_from_device
			self.local.config(height=3, width=18)
			self.local.grid(row=0, column=0, pady=10)

			self.random = tk.Button(self.mframe, bg='green', fg='white')
			self.random['text'] = 'Random wallpaper'
			self.random['command'] = lambda : self.change_wall('random')
			self.random.config(height=3, width=18)
			self.random.grid(row=1, column=0)
		else:
			self.filepath = tk.Label(self.mframe, bg='white', fg='black', anchor='w',
							borderwidth=1, relief='groove', wraplength=150)
			self.filepath['text'] = 'Select File'
			self.filepath.configure(width=22)
			self.filepath.grid(row=0, column=0, pady=10, padx=(2,5))

			self.select = tk.Button(self.mframe, image=clip_icon)
			self.select['command'] = self.select_wallpaper
			self.select.grid(row=0, column=1, pady=10)

			self.save = tk.Button(self.mframe, bg='green', fg='white')
			self.save['text'] = 'Change Wallpaper'
			self.save['command'] = lambda : self.change_wall('local')
			self.save.config(width=20)
			self.save.grid(row=1, column=0, pady=15 )

			self.back = tk.Button(self.mframe, image=back_icon)
			self.back['command'] = self.go_back
			self.back.grid(row=1, column=1, pady=15 )

	def choose_from_device(self):
		self.mframe.destroy()
		self.main = False
		self.path = ''
		self.main_frame()

	def select_wallpaper(self):
		self.path = filedialog.askopenfilename(initialdir=cwd,
			filetypes=[("Image files", ".jpg .png")])
		if self.path != '':
			self.filepath['text'] = self.path
	
	def change_wall(self, type_):
		if type_ == 'random':
			try:
				url = 'https://source.unsplash.com/random/1980x720'
				r = requests.get(url)
				with open('wallpaper.jpg', 'wb') as f:
					f.write(r.content)

				self.img_path = os.path.abspath('wallpaper.jpg')
			except:
				messagebox.showerror('No internet', 'Internet connection is required \nto download wallpaper')
				self.img_path = ''

		elif type_ == 'local':
			if self.path == '':
				messagebox.showerror('No image selected', 'Select a wallpaper first')
			self.img_path = self.path

		if self.img_path:
			SPI_DESKTOPWALLPAPER = 20
			if is_64bit_windows():
				ctypes.windll.user32.SystemParametersInfoW(SPI_DESKTOPWALLPAPER, 0, 
					self.img_path, 0)
			else:
				ctypes.windll.user32.SystemParametersInfoA(SPI_DESKTOPWALLPAPER, 0, 
					self.img_path, 0)

	def go_back(self):
		self.mframe.destroy()
		self.main = True
		self.path = ''
		self.main_frame()

# Main App -----------------------------------------------------------------------
root = tk.Tk()
root.geometry('250x200')
root.wm_title('Desktop Wallpaper Changer')

clip_icon = PhotoImage(file='icons/clip.png')
back_icon = PhotoImage(file='icons/back.png')

app = Application(master=root)
app.mainloop()