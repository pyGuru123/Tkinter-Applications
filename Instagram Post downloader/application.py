import os
import threading
import psutil
import subprocess
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox

import requests
import instaloader
from instaloader import Post, Profile
from PIL import Image, ImageTk

from customWidgets import CustomEntry, CountLabel, CustomLabel, CredentialWindow
from customWidgets import read_credentials, write_credentials

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.focus()
		self.draw_frames()
		self.draw_header_widgets()
		self.draw_body_widgets()

		self.bind('<Return>', self.search_user)
		self.master.protocol("WM_DELETE_WINDOW", self.stop_process)

	def draw_frames(self):
		self.title_frame = tk.Frame(self, width=300, height=50, bg='dodgerblue3')
		self.insta_frame = tk.Frame(self, width=100, height=100, bg='white')
		self.search_frame = tk.Frame(self, width=300, height=50, bg='white')
		tk.Label(self, width=56, bg='dodgerblue3').grid(row=2, column=0, columnspan=4)
		self.profile_frame = tk.Frame(self, width=200, height=150, bg='#b3cde0')
		self.info_frame = tk.Frame(self, width=200, height=150, bg='#b3cde0')
		self.download_frame = tk.Frame(self, width=400, height=50, bg='dodgerblue3')

		self.title_frame.grid(row=0, column=1, columnspan=3)
		self.search_frame.grid(row=1, column=1, columnspan=3)
		self.insta_frame.grid(row=0, column=0, rowspan=2)
		self.profile_frame.grid(row=3, column=0, columnspan=2)
		self.info_frame.grid(row=3, column=2, columnspan=2)
		self.download_frame.grid(row=4, column=0, columnspan=4)

		self.title_frame.grid_propagate(False)
		self.search_frame.grid_propagate(False)
		self.insta_frame.grid_propagate(False)
		self.profile_frame.grid_propagate(False)
		self.info_frame.grid_propagate(False)
		self.download_frame.grid_propagate(False)

	def draw_header_widgets(self):
		self.header = tk.Label(self.title_frame, text='InstaLoader',
						font=('Copperplate Gothic Light',25,'bold'), bg='white')
		self.header.grid(row=0, column=0, pady=(10,5), padx=15)

		self.username = tk.StringVar()
		self.entry = CustomEntry(self.search_frame, width=33, textvariable=self.username)
		self.entry.grid(row=0, column=0, pady=(8, 5), padx=(15,2))
		self.entry.bind('<Return>', self.search_user)

		self.search = tk.Button(self.search_frame, image=search_icon, 
							bg='white', cursor='hand2', command=self.search_user,
							relief=tk.FLAT)
		self.search.grid(row=0, column=1, pady=(8, 5), padx=2)

		self.settings = tk.Button(self.search_frame, image=settings_icon, 
							bg='white', cursor='hand2', command=self.ask_credentials,
							relief=tk.FLAT, height=45, width=30)
		self.settings.grid(row=0, column=2, pady=0, padx=0)

		self.left_label = tk.Label(self.insta_frame, width=1, height=8, bg='dodgerblue3')
		self.insta_label = tk.Label(self.insta_frame, width=90, height=97, image=insta_icon,
							bg='white')

		self.left_label.grid(row=0, column=0)
		self.insta_label.grid(row=0, column=1)

	def draw_body_widgets(self):
		self.profile_name = CustomLabel(self.profile_frame, width=25, height=2, anchor='c')
		self.profile_pic = tk.Button(self.profile_frame, text='click to Open',
							compound=tk.TOP, relief=tk.FLAT)

		self.profile_name.grid(row=0, column=0)
		self.profile_pic.grid(row=1, column=0, padx=6, pady=8)
		self.profile_pic.grid_forget()

		self.followers_label = CustomLabel(self.info_frame)
		self.following_label = CustomLabel(self.info_frame)
		self.post_label = CustomLabel(self.info_frame)
		self.followers_count = CountLabel(self.info_frame)
		self.following_count = CountLabel(self.info_frame)
		self.post_count = CountLabel(self.info_frame)

		self.followers_label.grid(row=0, column=0, padx=(15,2), pady=(5,2))
		self.following_label.grid(row=1, column=0, padx=(15,2), pady=2)
		self.post_label.grid(row=2, column=0, padx=2, pady=(15,2))
		self.followers_count.grid(row=0, column=1, padx=2, pady=(5,2))
		self.following_count.grid(row=1, column=1, padx=2, pady=2)
		self.post_count.grid(row=2, column=1, padx=2, pady=2)

		self.download_button = tk.Button(self.download_frame, bg='green',
				text='Download all posts', fg='white', width=20)
		self.download_button.grid(row=0, column=0, pady=10, padx=30)
		self.download_button.grid_forget()

		self.stop_button = tk.Button(self.download_frame, bg='green',
				text='Quit Application', fg='white', width=20,
				command=self.stop_process)
		self.stop_button.grid(row=0, column=1, pady=10, padx=40)
		self.stop_button.grid_forget()


	def search_user(self, event=None):
		self.search.config(state=tk.DISABLED)

		thread = threading.Thread(target=self.search_user_profile)
		thread.start()
		self.poll_thread(thread)

	def poll_thread(self, thread):
		if thread.is_alive():
			self.after(100, lambda : self.poll_thread(thread))
		else:
			self.search.config(state=tk.NORMAL)

	def search_user_profile(self):
		self.user = self.username.get()
		if self.user and self.user != 'Enter Instagram Username':
			account_details = read_credentials()
			if account_details:
				username, password = account_details
			else:
				self.ask_credentials()
				account_details = read_credentials()
				if account_details:
					username, password = account_details
				else:
					username, password = None, None


			if username and password:
				try:
					self.loader = instaloader.Instaloader()
					self.loader.login(username, password)

					self.profile = Profile.from_username(self.loader.context, self.user)
					img_url = self.profile.get_profile_pic_url()
					name = self.profile.full_name
					following = self.profile.get_followees().count
					followers = self.profile.get_followers().count
					posts= self.profile.get_posts().count

					followers = self.update_numbers(followers)
					following = self.update_numbers(following)
					posts = self.update_numbers(posts)

					self.profile_name['text'] = name
					self.followers_label['text'] = 'Followers'
					self.following_label['text'] = 'Following'
					self.post_label['text'] = 'Posts'
					self.followers_count['text'] = followers
					self.following_count['text'] = following
					self.post_count['text'] = posts

					self.update_idletasks()

					r = requests.get(img_url)
					with open('profile.jpg', 'wb') as file:
						file.write(r.content)

					self.profile_pic.grid(row=1, column=0, padx=6, pady=2)
					self.profile_pic.config(width=180, height=105)
					self.profile_image = ImageTk.PhotoImage(Image.open('profile.jpg').resize((160,95)))
					self.profile_pic['image'] = self.profile_image
					self.profile_pic['command'] = self.display_profile_pic

					self.download_button.grid(row=0, column=0, pady=10, padx=30)
					self.stop_button.grid(row=0, column=1, pady=10, padx=40)

					self.download_button['command'] = self.download_all_posts
				except instaloader.exceptions.InstaloaderException:
					messagebox.showerror('Instaloader', 'No internet connection')
				except instaloader.exceptions.ProfileNotExistsException:
					messagebox.showerror('Instaloader', 'Profile does not exist')
				except instaloader.exceptions.InstaloaderException:
					messagebox.showerror('Instaloader', 'Incorrect username or password')
		else:
			print('Enter Insta Username')

	def display_profile_pic(self):
		self.after(100, lambda : subprocess.run(['explorer', 'profile.jpg']))

	def ask_credentials(self):
		CredentialWindow()

	def download_all_posts(self):
		print('starting')
		self.stop_button['text'] = 'Stop Download & Quit'
		self.search.config(state=tk.DISABLED)

		thread1 = threading.Thread(target=self.download_all)
		thread1.start()
		self.poll_thread(thread1)

	def download_all(self):
		self.loader.download_profile(self.user, download_stories=False, download_tagged=False)

	def stop_process(self):
		PROCNAME = "python.exe"

		for proc in psutil.process_iter():
			# check whether the process name matches
			if proc.name() == PROCNAME:
				proc.kill()

	def update_numbers(self, num):
		if num >= 1000000:
			num /= 1000000
			num = f'{num:.1f}M'
		elif num >= 1000:
			num /= 1000
			num = f'{num:.1f}K'
		else:
			num = str(num)

		return num

# mahakaal_ka_drbar
# prajjwalpathak35

if __name__ == '__main__':
	if not os.path.exists('files/'):
		os.mkdir('files')

	root = tk.Tk()
	root.geometry('400x320+400+200')
	root.title('Instagram downloader')
	root.resizable(0,0)

	search_icon = PhotoImage(file='icons/search.png')
	insta_icon = PhotoImage(file='icons/insta.png')
	settings_icon = PhotoImage(file='icons/settings.png')
	# profile_img = PhotoImage(file='profile.png')

	app = Application(master=root)
	app.mainloop()