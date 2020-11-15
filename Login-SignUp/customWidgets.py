import tkinter as tk
from tkinter import PhotoImage

class CustomEntry(tk.Entry):
	def __init__(self, parent, *args, **kwargs):
		tk.Entry.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.text = kwargs.get('text', '')
		self.color = 'gray60'
		self.bind('<FocusOut>', self.add_placeholder)
		self.bind('<FocusIn>', self.clear_placeholder)

		self.configure(fg=self.color)
		self.insert(0, self.text)

	def add_placeholder(self, event=None):
		if not self.get():
			self.configure(fg=self.color)
			self.insert(0, self.text)

	def clear_placeholder(self, event):
		if event and self.get() == self.text:
			self.delete('0', 'end')
			self.configure(fg="black")

class CustomPassword(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.frame = tk.Frame(background="white", borderwidth=1, relief=tk.FLAT,
                         highlightthickness=0)
		self.frame.grid(row=0, column=0)

		self.pwd_hidden = True

		self.hide = PhotoImage(file='icons/hide.png')
		self.show = PhotoImage(file='icons/show.png')

		self.entry = tk.Entry(self.frame, width=23, highlightthickness=0, show='*')
		self.btn = tk.Button(self.frame, image=self.hide, relief=tk.FLAT, command=self.hide_unhide_pwd)

		self.entry.grid(row=0, column=0) 
		self.btn.grid(row=0, column=1)

	def hide_unhide_pwd(self):
		if self.pwd_hidden == True:
			self.pwd_hidden = False
			self.entry.config(show='')
			self.btn['image'] = self.hide
		else:
			self.pwd_hidden = True
			self.entry.config(show='*')
			self.btn['image'] = self.show