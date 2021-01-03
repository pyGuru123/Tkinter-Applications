import os
import shelve
import requests
import threading
import subprocess
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import PhotoImage
from tkinter import messagebox

class CustomEntry(tk.Entry):
	def __init__(self, parent, *args, **kwargs):
		tk.Entry.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.bind('<FocusOut>', self.add_placeholder)
		self.bind('<FocusIn>', self.clear_placeholder)

		self.configure(fg="gray70")
		self.insert(0, 'Enter Image URL')

	def add_placeholder(self, event=None):
		if not self.get():
			self.configure(fg="gray70")
			self.insert(0, 'Enter Image URL')

	def clear_placeholder(self, event):
		if event and self.get() == 'Enter Image URL':
			self.delete('0', 'end')
			self.configure(fg="black")

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master.focus_set()
		self.master = master
		self.grid()

		self.filesize = 0
		self.url = tk.StringVar()
		self.url.set('')
		self.move_ahead = True

		self.draw_title_frame()
		self.draw_search_frame()
		self.draw_download_frame()

	def draw_title_frame(self):
		self.title_frame = tk.Frame(self, bg='#0876ee', width=440, height=60)
		self.title_frame.grid(row=0, column=0, pady=5)
		self.title_frame.grid_propagate(False)
		self.title = tk.Label(self.title_frame, text='      Image Downloader',
							fg='white', bg='#0876ee', font=('verdana',18,'bold'),
							width=450, height=50, image=img_downloader_icon, compound=tk.LEFT,
							anchor='w')
		self.title.grid(row=0, column=0, padx=5, ipadx=20)

	def draw_search_frame(self):
		self.search_frame = tk.Frame(self, width=440, height=70, highlightthickness=1,
							highlightbackground='#ff5f37')
		self.search_frame.grid(row=1, column=0, pady=(5,0))
		self.search_frame.grid_propagate(False)

		self.entry = CustomEntry(self.search_frame, width=52, textvariable=self.url)
		self.entry.grid(row=0, column=0, columnspan=3, pady=20, padx=(20,10))
		self.entry.bind('<Return>', self.start_action)

		self.download = tk.Button(self.search_frame, image=download_icon, 
							fg='white', cursor='hand2', command=self.start_action,
							relief=tk.FLAT)
		self.download.grid(row=0, column=4, pady=20, padx=(30,10))

	def draw_download_frame(self):
		self.download_frame = tk.Frame(self, width=440, height=190, highlightthickness=1,
							highlightbackground='#ff5f37')
		self.download_frame.grid(row=2, column=0, pady=0)
		self.download_frame.grid_propagate(False)

		self.label = tk.Label(self.download_frame, text='Enter image url, press enter',
					font=('verdana', 9), width=50)
		self.label.grid(row=0, column=0, padx=10, pady=5, columnspan=4)

		self.progressbar = ttk.Progressbar(self.download_frame, length=400,
								orient=tk.HORIZONTAL,mode = 'determinate')
		self.progressbar.grid(row=1, column=0, padx=10, pady=5, columnspan=4)
		self.progressbar.grid_forget()

		self.preview = tk.Button(self.download_frame, text='Click to Open', compound=tk.TOP)
		self.preview.grid(row=2, column=2, columnspan=2)
		self.preview.grid_forget()

		self.clear = ttk.Button(self.download_frame, text='Clear', command=self.clear_screen)
		self.clear.grid(row=2, column=0, columnspan=2)
		self.clear.grid_forget()

	def start_action(self, event=None):
		self.download.config(state=tk.DISABLED)
		self.forget_everything()
		self.move_ahead = True

		thread = threading.Thread(target=self.AsyncAction)
		thread.start()
		self.poll_thread(thread)

	def poll_thread(self, thread):
		if thread.is_alive():
			self.after(100, lambda : self.poll_thread(thread))
		else:
			self.label['text'] = 'Enter image url, press enter'
			self.download.config(state=tk.NORMAL)

			if self.move_ahead:
				self.clear.grid(row=2, column=0, columnspan=2)
				self.preview.grid(row=2, column=2, columnspan=2)

				image = f'image{self.image_index}.jpg'
				self.image = ImageTk.PhotoImage(Image.open(image).resize((150,90)))
				self.preview.config(width=180, height=100)
				self.preview['image'] = self.image
				self.preview['command'] = self.display_image
			
	def display_image(self):
		image = f'image{self.image_index}.jpg'
		self.after(100, lambda : subprocess.run(['explorer', image]))

	def AsyncAction(self):
		url = self.url.get()
		if url:
			self.label['text'] = 'your image is now downloading...'
			self.progressbar.grid(row=1, column=0, padx=10, pady=5, columnspan=4)
			try:
				response = requests.get(url, stream=True)
				self.filesize = len(response.content)

				with shelve.open('files/index', writeback = True) as shelf:
					self.image_index = shelf['index']
					shelf['index'] = self.image_index + 1

				file_name = f'image{self.image_index}.jpg'
				with open(file_name, "wb") as f:
					dl = 0
					for data in response.iter_content(chunk_size=1024):
						dl += len(data)
						f.write(data)
						self.progressbar['value'] = 4 * int(dl * 100 / self.filesize)
						self.update_idletasks()

				if os.stat(file_name).st_size == 0:
					os.unlink(file_name)
					raise Exception
			except:
				self.move_ahead = False
				self.forget_everything()
				self.download.config(state=tk.NORMAL)
				messagebox.showerror('Image Downloader', 'Cannot download the image')


	def forget_everything(self):
		self.progressbar['value'] = 0
		self.preview['image'] = ''

		self.progressbar.grid_forget()
		self.preview.grid_forget()
		self.clear.grid_forget()
		self.image = None

	def clear_screen(self):
		self.label['text'] = 'Enter image url, press enter'
		self.forget_everything()
		self.url.set('')

				
# https://wallpaperaccess.com/full/33115.jpg


if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('440x320')
	root.title('Image Downloader')
	root.resizable(0,0)

	if not os.path.exists('files/index.dat'):
		os.mkdir('files/')
		with shelve.open('files/index', 'n') as shelf:
			shelf['index'] = 0

	img_downloader_icon = PhotoImage(file='icons/img_downloader.png')
	download_icon = PhotoImage(file='icons/download.png')

	app = Application(master=root)
	app.mainloop()