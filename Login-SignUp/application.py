# Login & Signup

import os
import re
import json
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage

from customWidgets import CustomEntry, CustomPassword
from credentials import Database, encode_password, decode_password



class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.pack()

		self.db = Database()
		self.all_credentials = self.db.fetch_all_creds()

		self._attributes()
		self.draw_home_frame()

	def _attributes(self):
		self.on_home = True
		self.pwd_hidden = True
		self.username = tk.StringVar()
		self.email_id = tk.StringVar()
		self.password = tk.StringVar()
		self.captcha = None

		self.current_user = None

	def draw_home_frame(self):
		self.head = tk.Frame(self, width=250, height=150)
		self.body = tk.Frame(self, width=250, height=100)

		self.head.grid(row=0, column=0)
		self.body.grid(row=1, column=0)

		self.head.grid_propagate(False)
		self.body.grid_propagate(False)

		self.header = tk.Label(self.head, width=120, height=120, image=avtar,
							text='\nAuthenticator', compound=tk.TOP, fg='black',
							font=('Lucida Bright', 12, 'bold'))
		self.header.grid(row=0, column=0, pady=8, padx=60)

		self.signup_page = ttk.Button(self.body, text='New User ?\n   SignUp', command=self.draw_signup_frame,
							width=30)
		self.login_page = ttk.Button(self.body, text='Login', command=self.draw_login_frame,
							width=30)

		self.signup_page.grid(row=0, column=0, padx=28, pady=5)
		self.login_page.grid(row=1, column=0, padx=28, pady=8)

		if len(self.all_credentials) == 0:
			self.login_page['state'] = 'disabled'
		else:
			self.login_page['state'] = 'enabled'

	def draw_signup_frame(self):
		self.head.destroy()
		self.body.destroy()
		self._attributes()

		# header
		self.head = tk.Frame(self, width=250, height=40)
		self.head.grid(row=0, column=0)
		self.head.grid_propagate(False)
		
		self.header = tk.Label(self.head, text='Create Your Account', fg='dodgerblue2',
					font=('Lucida Bright', 16))
		self.header.grid(row=0, column=0, padx=15, pady=5)

		# body
		self.body = tk.Frame(self, width=250, height=210)
		self.body.grid(row=1, column=0)
		self.body.grid_propagate(False)

		self.account_frame = ttk.LabelFrame(self.body, text='Account', width=240, height=110)
		self.captcha_frame = ttk.LabelFrame(self.body, text='Captcha', width=240, height=55)
		self.back_btn = tk.Button(self.body, image=back, command=self.to_home_page, relief=tk.FLAT)
		self.submit_btn = ttk.Button(self.body, text='Submit', width=20, command=self.register_user)

		self.account_frame.grid(row=0, column=0, padx=5, pady=(5,2), columnspan=2)
		self.captcha_frame.grid(row=1, column=0, padx=5, columnspan=2)
		self.back_btn.grid(row=2, column=0, pady=5)
		self.submit_btn.grid(row=2, column=1, pady=5)

		self.account_frame.grid_propagate(False)
		self.captcha_frame.grid_propagate(False)

		self.nameLabel = ttk.Label(self.account_frame, text='Username', anchor='w', width=9)
		self.nameEntry = ttk.Entry(self.account_frame, textvariable=self.username, width=26)
		self.emailLabel = ttk.Label(self.account_frame, text='Email', anchor='w', width=9)
		self.emailEntry = ttk.Entry(self.account_frame, textvariable=self.email_id, width=26)
		self.pwdLabel = ttk.Label(self.account_frame, text='Password', anchor='w', width=9)
		self.pwdEntry = ttk.Entry(self.account_frame, textvariable=self.password, width=23, show='*')
		self.pwdState = tk.Button(self.account_frame, image=show, relief=tk.FLAT, command=self.hide_unhide_pwd)

		self.nameLabel.grid(row=0, column=0, padx=3, pady=3)
		self.nameEntry.grid(row=0, column=1, padx=3, pady=3, columnspan=2, sticky='w')
		self.emailLabel.grid(row=1, column=0, padx=3, pady=3)
		self.emailEntry.grid(row=1, column=1, padx=3, pady=3, columnspan=2, sticky='w')
		self.pwdLabel.grid(row=2, column=0, padx=3, pady=3)
		self.pwdEntry.grid(row=2, column=1, padx=(3,0), pady=3, columnspan=1, sticky='w')
		self.pwdState.grid(row=2, column=2)

		self.captcha = self.generate_captcha()
		self.captcha_label = tk.Label(self.captcha_frame, text=self.captcha, width=8, bg='coral2', fg='white')
		self.captcha_refresh = tk.Button(self.captcha_frame, image=recaptcha, relief=tk.FLAT, command=self.generate_captcha)
		self.captcha_entry = ttk.Entry(self.captcha_frame, width=10)

		self.captcha_label.grid(row=0, column=0, padx=(10,5))
		self.captcha_refresh.grid(row=0, column=1, padx=20)
		self.captcha_entry.grid(row=0, column=2, padx=5)
		

	def draw_login_frame(self):
		self.head.destroy()
		self.body.destroy()

		self.head = tk.Frame(self, width=250, height=150)
		self.body = tk.Frame(self, width=250, height=100)

		self.head.grid(row=0, column=0)
		self.body.grid(row=1, column=0)

		self.head.grid_propagate(False)
		self.body.grid_propagate(False)

		self.header = tk.Label(self.head, width=100, height=140, image=avtar,
							text='\nLogin', compound=tk.TOP, fg='black',
							font=('Arial', 12, 'bold'), cursor='hand2')
		self.header.bind("<Button-1>", self.to_home_page)
		self.header.grid(row=0, column=0, pady=8, padx=70)

		if self.on_home:
			self.email_ = CustomEntry(self.body, text='Email', width=26, textvariable=self.email_id)
			self.email_.grid(row=0, column=0, padx=(25,12), pady=20)

			self.send = tk.Button(self.body, image=send, relief=tk.FLAT, command=self.fetch_email)
			self.send.grid(row=0, column=1, padx=10, pady=20)

			self.not_registered = tk.Label(self.body, text='Not a registered user, SignUp here',
						font=('Arial', 8, 'underline'), fg='blue', cursor='hand2')
			self.not_registered.bind("<Button-1>", self.to_signup)
			self.not_registered.grid(row=1, column=0, columnspan=2)
			
		else:
			self.header['text'] = '\nHello ' + self.username.get()
			self.pass_ = CustomEntry(self.body, text='Password', width=26, textvariable=self.password)
			self.pass_.grid(row=0, column=0, padx=20, pady=20)

			self.send = tk.Button(self.body, image=send, relief=tk.FLAT, command=self.verify_login)
			self.send.grid(row=0, column=1, padx=10, pady=20)

	# custom functions

	def hide_unhide_pwd(self):
		if self.pwd_hidden == True:
			self.pwd_hidden = False
			self.pwdEntry.config(show='')
			self.pwdState['image'] = hide
		else:
			self.pwd_hidden = True
			self.pwdEntry.config(show='*')
			self.pwdState['image'] = show

	def to_home_page(self, event=None):
		self._attributes()

		self.head.destroy()
		self.body.destroy()
		self.draw_home_frame()

	def register_user(self):
		username = self.username.get()
		email = self.email_id.get()
		password = self.password.get()
		captcha = self.captcha_entry.get()

		if not username:
			messagebox.showinfo('Authenticator', 'Username required')
		elif not email:
			messagebox.showinfo('Authenticator', 'Email required')
		elif email and not valid_email(email):
			messagebox.showerror('Authenticator', 'Invalid email')
		elif not password:
			messagebox.showinfo('Authenticator', 'Password required')
		elif not captcha:
			messagebox.showinfo('Authenticator', 'Fill captcha to continue')
		else:
			if str(eval(self.captcha)) == captcha:
				password = encode_password(password)
				self.db.insert_credential((username, email, password))
				self.all_credentials = self.db.fetch_all_creds()
				messagebox.showinfo('Authenticator', 'Registration Successfull')

				self._attributes()
				self.current_user = (username, email, password)
				self.on_home = False
				self.draw_login_frame()
				self.header['text'] = f'Hello {username}'
				self.header.config(font=('Arial', 10, 'bold'))
			else:
				self.captcha_entry.delete(0, tk.END)
				self.generate_captcha()

	def generate_captcha(self):
		captcha = str(random.randint(1,100)) + ' ' + random.choice(['+','-','*']) + ' ' + str(random.randint(1,100))
		if self.captcha is not None:
			self.captcha_label['text'] = captcha
			self.captcha = captcha
		return captcha

	def to_home(self):
		self.on_home = True
		self.email_id.set('')
		self.body.destroy()
		self.draw_widgets()

	def to_signup(self, event):
		self.draw_signup_frame()

	def fetch_email(self):
		email = self.email_.get()
		if email not in (' ', 'Email'):
			data = self.db.fetch_credential(email)
			if data is not None:
				self.current_user = data
				self.on_home = False
				self.password.set('')
				self.draw_login_frame()
				self.header['text'] = f'\nHello {self.current_user[0]}'
				self.header.config(font=('Arial', 9, 'bold'))
			else:
				messagebox.showerror('Authenticator', 'Not registered')

	def verify_login(self):
		password = decode_password(self.current_user[2])
		if self.pass_.get() == password:
			self.is_success()
		else:
			messagebox.showerror('Authenticator', 'Incorrect Password')
			self.pass_.delete(0, tk.END)

	def is_success(self):
		self.head.destroy()
		self.body.destroy()

		self.page = tk.Frame(self, width=250, height=250, bg='white')
		self.page.grid(row=0, column=0)
		self.page.grid_propagate(False)

		self.frame = 0
		self.should_continue = True
		self.label = tk.Label(self.page, image=success_list[self.frame])
		self.label.grid(row=0, column=0, pady=20, padx=50)

		self.after(0, self.update)

	def update(self):
		if self.frame <= len(success_list)-2:
			self.frame += 1
		else:
			self.should_continue = False

			l2 = tk.Label(self.page, text='LoggedIn Successfully', fg='dodgerblue2',
						font=('Lucida Bright', 12, 'bold'))
			l2.grid(row=1, column=0)

			self.write_current_user_record()
			self.after(2000, self.quit)

		if self.should_continue:
			self.label.configure(image=success_list[self.frame])
			self.after(20, self.update)

	def write_current_user_record(self):
		dct = {
			'username' : self.current_user[0],
			'email'    : self.current_user[1],
			'password' : str(self.current_user[2])
		}

		with open('files/current_user.json', 'w') as file:
			json.dump(dct, file, indent=4)

def valid_email(email):
	email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
	if re.fullmatch(email_regex, email):
		return True
	return False

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('250x250+500+250')
	root.title('Authenticator')
	root.resizable(0,0)

	random_int = random.randint(1,5)
	filename = f'icons/avtar{random_int}.png'

	avtar = PhotoImage(file=filename)
	send = PhotoImage(file='icons/send.png')
	back = PhotoImage(file='icons/back.png')
	hide = PhotoImage(file='icons/hide.png')
	show = PhotoImage(file='icons/show.png')
	recaptcha = PhotoImage(file='icons/recaptcha.png')
	success_list = [PhotoImage(file='success/'+img) for img in os.listdir('success/')]

	app = Application(master=root)
	app.mainloop()