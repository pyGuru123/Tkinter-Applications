import os
import json
import tkinter as tk

class CustomEntry(tk.Entry):
	def __init__(self, parent, *args, **kwargs):
		tk.Entry.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.bind('<FocusOut>', self.add_placeholder)
		self.bind('<FocusIn>', self.clear_placeholder)

		self.configure(fg="gray68")
		self.insert(0, 'Enter Instagram Username')

	def add_placeholder(self, event=None):
		if not self.get():
			self.configure(fg="gray68")
			self.insert(0, 'Enter Instagram Username')

	def clear_placeholder(self, event):
		if event and self.get() == 'Enter Instagram Username':
			self.delete('0', 'end')
			self.configure(fg="black")

class CustomLabel(tk.Label):
	def __init__(self, parent, *args, **kwargs):
		tk.Label.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		width = kwargs.get('width', 8)
		height = kwargs.get('height', 1)
		anchor = kwargs.get('anchor', 'e')
		self.configure(width=width, font=('verdana', 9, 'bold'),
					 bg='#b3cde0', anchor=anchor, fg='black')

class CountLabel(tk.Label):
	def __init__(self, parent, *args, **kwargs):
		tk.Label.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.configure(bg='#b3cde0', width=8, height=2,
				font=('verdana', 12, 'bold'))

class CredentialWindow(tk.Toplevel):
	def __init__(self):
		super(CredentialWindow, self).__init__()
		self.title('Credentials')
		self.geometry('300x150+450+345')
		self.resizable(0,0)

		self.draw_widgets()
		self.protocol("WM_DELETE_WINDOW", self.save_credentials)

	def draw_widgets(self):
		tk.Label(self, text='Enter your instagram details here', fg='black',
				font=('verdana', 10, 'bold')).grid(row=0, column=0, padx=25, pady=5,
						columnspan=4)

		pady = 10
		tk.Label(self, text='Username', font=('verdana', 9, 'bold')).grid(
							row=1, column=0, pady=pady, columnspan=2)
		tk.Label(self, text='Password', font=('verdana', 9, 'bold')).grid(
							row=2, column=0, pady=pady, columnspan=2)

		self.username =tk.StringVar()
		self.password =tk.StringVar()

		account_details = read_credentials()
		if account_details:
			username, password = account_details
			self.username.set(username)
			self.password.set(password)

		tk.Entry(self, width=20, textvariable=self.username).grid(row=1, column=2,
							 columnspan=2, pady=pady)
		tk.Entry(self, width=20, textvariable=self.password).grid(row=2, column=2,
							 columnspan=2, pady=(pady-5))

		tk.Button(self, text='Save',bg='green', relief=tk.FLAT,
					fg='white', width=8, command=self.save_credentials
					).grid(row=3, column=1, columnspan=2, pady=5)

	def save_credentials(self):
		username = self.username.get()
		password = self.password.get()

		if username and password:
			data = {
					'username' : username,
					'password' : password
			}

			write_credentials(data)

			self.destroy()

def read_credentials():
	json_file = 'files/credentials.json'

	if os.path.exists(json_file):
		with open(json_file, 'r') as file:
			dct = json.load(file)

		return dct['username'], dct['password']
	else:
		return None

def write_credentials(data):
	json_file = 'files/credentials.json'
	with open(json_file, 'w') as file:
		json.dump(data, file)