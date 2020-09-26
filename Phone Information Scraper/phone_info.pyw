from scraper import scrape_phone_info

import re
import tkinter as tk 
from tkinter import PhotoImage
from tkinter import messagebox

phone_regex = re.compile(r'^\d{10}$')

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.pack()

		self.draw_frame()

	def draw_frame(self):
		self.phone = tk.StringVar()
		self.entry = tk.Entry(self, width=25)
		self.entry['textvariable'] = self.phone
		self.entry.grid(row=0, column=0)

		self.search = tk.Button(self, image=search_icon)
		self.search['command'] = lambda : self.get_phone_info(self.phone.get())
		self.search.grid(row=0, column=1)

		self.scroll = tk.Scrollbar(self, orient = tk.VERTICAL)
		self.scroll.grid(row=0, column=2, sticky='ns', padx=0, rowspan=2)

		self.output = tk.Text(self, fg='green')
		self.output.insert(tk.END, 'Enter your 10 digit phone number to scrape related info')
		self.output.configure(width=35, height=20, state='disabled')
		self.output.grid(row=1, column=0, columnspan=2, pady=15)

		self.output.config(yscrollcommand=self.scroll.set)
		self.scroll.config(command = self.output.yview)

	def get_phone_info(self, phone_number):
		if re.match(phone_regex, phone_number):
			self.result = scrape_phone_info(phone_number)
			if self.result == 'ConnectionError':
				messagebox.showerror('No internet', 'ConnectionError : Internet connection is required')
				self.result = 'No internet connection\n'
		else:
			self.result = 'Insert a valid 10 digit phonenumber\n'

		self.output.configure(state='normal')
		self.output.delete('1.0', tk.END)
		self.output.insert(tk.END, self.result)
		self.output.configure(state='disabled')


if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('300x380')
	root.wm_title('Phone Info Scraper')

	search_icon = PhotoImage(file='icons/search.png')

	app = Application(master=root)
	app['bg'] = 'slate gray'
	app.mainloop()