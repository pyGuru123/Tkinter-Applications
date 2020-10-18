import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import messagebox

import pafy
import youtube_dl

# if you get api limit exceeded error, get an api key and paste
# here as a string value
# pafy.set_api_key(key)

# sample video url
# https://www.youtube.com/watch?v=CjeYOtL6ORE

cwd = os.getcwd()

class CustomEntry(tk.Entry):
	def __init__(self, parent, *args, **kwargs):
		tk.Entry.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.bind('<FocusOut>', self.add_placeholder)
		self.bind('<FocusIn>', self.clear_placeholder)

		self.configure(fg="gray70")
		self.insert(0, 'Enter Video URL')

	def add_placeholder(self, event=None):
		if not self.get():
			self.configure(fg="gray70")
			self.insert(0, 'Enter Video URL')

	def clear_placeholder(self, event):
		if event and self.get() == 'Enter Video URL':
			self.delete('0', 'end')
			self.configure(fg="black")

# Application Class -----------------------------------------------

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.master.focus_set()
		self.pack()

		self.url = ''
		self.video_quality = tk.StringVar()
		self.filesize = 0

		self.draw_title_frame()
		self.draw_main_frame()

		self.bind('<Return>', self.search_video)

	def draw_title_frame(self):
		self.title_frame = tk.Frame(self, bg='red', width=440, height=60)
		self.title_frame.grid(row=0, column=0, columnspan=5, pady=5)
		self.title_frame.grid_propagate(False)
		self.title = tk.Label(self.title_frame, text=' SaveFromYT - Youtube Audio/Video Downloader',
							fg='white', bg='red', font=('Times', 14),
							width=450, height=50, image=youtube_icon, compound=tk.LEFT,
							anchor = 'w')
		self.title.grid(row=0, column=0, padx=5, ipadx=20)

	def draw_main_frame(self):
		self.main_frame = tk.Frame(self, width=440, height=240, highlightthickness=1,
							highlightbackground='red')
		self.main_frame.grid(row=1, column=0, columnspan=5, pady=5, rowspan=3)
		self.main_frame.grid_propagate(False)

		self.entry = CustomEntry(self.main_frame, width=52)
		self.entry.grid(row=0, column=0, columnspan=3, pady=100, padx=(20,10))
		self.entry.bind('<Return>', self.search_video)

		self.search = tk.Button(self.main_frame, image=search_icon, 
							fg='white', cursor='hand2', command=self.search_video,
							relief=tk.FLAT)
		self.search.grid(row=0, column=4, pady=100, padx=(30,10))

	def draw_download_frame(self):
		self.main_frame.destroy()

		self.info_frame = tk.Frame(self, width=150, height=173, highlightthickness=1,
							highlightbackground='red')
		self.info_frame.grid(row=1, column=0, columnspan=2)
		self.info_frame.grid_propagate(False)

		self.video_frame = tk.Frame(self, width=290, height=173, highlightthickness=1,
							highlightbackground='red')
		self.video_frame.grid(row=1, column=2, columnspan=3)
		self.video_frame.grid_propagate(False)

		self.audio_frame = tk.Frame(self, width=370, height=67, highlightthickness=1,
							highlightbackground='red')
		self.audio_frame.grid(row=2, column=0, columnspan=4)
		self.audio_frame.grid_propagate(False)

		self.back_frame = tk.Frame(self, width=70, height=67, highlightthickness=1,
							highlightbackground='red')
		self.back_frame.grid(row=2, column=4)
		self.back_frame.grid_propagate(False)

	def draw_download_widgets(self):
		# self.info_frame

		self.title = tk.Label(self.info_frame, width=20, height=3, bg='red',
					wraplength=120, fg='white')
		self.title.grid(row=0, column=0, padx=1, pady=2)

		self.views = tk.Label(self.info_frame, width=20, height=2, bg='red',
					fg='white')
		self.views.grid(row=1, column=0, padx=1, pady=1)

		self.duration = tk.Label(self.info_frame, width=20, height=2, bg='red',
					fg='white')
		self.duration.grid(row=2, column=0, padx=1, pady=1)

		self.published = tk.Label(self.info_frame, width=20, height=2, bg='red',
					fg='white')
		self.published.grid(row=3, column=0, padx=1, pady=1)

		# self.video_frame

		self.video_quality.set(self.option_streams[0])
		self.options = tk.OptionMenu(self.video_frame, self.video_quality,
						*self.option_streams)
		self.options.config(bg='red', fg='white')
		self.options['menu'].config(bg='red', fg='white')
		self.options.grid(row=0, column=0, padx=50, pady=20, columnspan=5)

		self.video_dwn = tk.Button(self.video_frame, text='Download Video',
							command=self.download_video, bg='red', fg='white',
							width=15, cursor='hand2')
		self.video_dwn.grid(row=1, column=0, padx=50, pady=10, columnspan=5)

		# self.audio_frame

		self.audio_dwn = tk.Button(self.audio_frame, text='Download MP3',
							command=self.download_mp3, bg='red', fg='white',
							width=15, cursor='hand2')
		self.audio_dwn.grid(row=0, column=0, padx=20, pady=20)

		# self.back_frame
		self.back = tk.Button(self.back_frame, text='back', image=back_icon,
							command=self.go_back, relief=tk.FLAT)
		self.back.grid(row=0, column=0, pady=10, padx=10)

	def search_video(self, event=None):
		self.url = self.entry.get()
		self.master.focus_set()
		
		if self.url and ' ' not in self.url:
			try:
				video = pafy.new(self.url)
				self.video_title = video.title
				duration = video.duration
				views = video.viewcount
				published = video.published
				thumbnail = video.thumb
				self.streams = video.streams
				self.option_streams = self.streams[::-1]

				self.draw_download_frame()
				self.draw_download_widgets()

				self.title['text'] = self.video_title[:50]
				self.views['text'] = f'Views : {views:,}'
				self.duration['text'] = f'Length : {duration}'
				self.published['text'] = f'Pub : {published[:10]}'
			except OSError:
				messagebox.showerror('SaveFromYT', 'Cannot extract data')
			except ValueError:
				messagebox.showerror('SaveFromYT', 'Invalid URL')
			except:
				messagebox.showerror('SaveFromYT', 'Cannot connect with internet')

	def download_video(self):
		filetypes = [('MP4', '.mp4')]
		filepath = filedialog.asksaveasfilename(initialdir=cwd, 
						initialfile=self.video_title[:25]+'.mp4',
						filetypes=filetypes)
		if filepath:
			vq = self.video_quality.get()
			l = len(self.streams)
			opts = [str(stream) for stream in self.option_streams]
			stream = self.streams[opts.index(vq) - l + 1]
			self.filesize = stream.get_filesize()

			self.sizelabel = tk.Label(self.video_frame, bg='red', fg='white',
							text=f'Filesize : {self.filesize/(1024*1024):.2f} Mb')
			self.sizelabel.grid(row=2, column=0, pady=5)
			self.pb = ttk.Progressbar(self.video_frame, orient=tk.HORIZONTAL, 
							mode='determinate', length=100)
			self.pb.grid(row=2, column=2, columnspan=3, pady=5)

			try:
				stream.download(quiet=True, callback=self.download_callback,
								filepath=filepath)
				messagebox.showinfo('SaveFromYT', 'Video Downloaded Successfully')
			except:
				messagebox.showerror('SaveFromYT', 'Cannot connect with internet')
			
			self.pb.destroy()
			self.sizelabel.destroy()
			

	def download_callback(self, total, recvd, ratio, rate, eta):
		perc = (recvd / total) * 100
		self.pb['value'] = int(perc)
		self.update()

	def download_mp3(self):
		filetypes = ['MP3', '.mp3']
		filepath = filedialog.asksaveasfilename(initialdir=cwd, 
						initialfile=''.join(self.video_title[:25]+'.mp3'))
		if filepath:
			ydl_opts = {
				'format': 'bestaudio/best',
				'outtmpl' : filepath,
				'postprocessors': [{
					'key': 'FFmpegExtractAudio',
					'preferredcodec': 'mp3',
					'preferredquality': '192'
				}],
				'postprocessor_args': [
					'-ar', '16000'
				],
				'prefer_ffmpeg': True,
				'keepvideo': True,
				'progress_hooks': [self.download_hook]
			}

			try:
				self.pb = ttk.Progressbar(self.audio_frame, orient=tk.HORIZONTAL, 
							mode='determinate', length=100)
				self.pb.grid(row=0, column=2, pady=20, padx=20)

				with youtube_dl.YoutubeDL(ydl_opts) as ydl:
					ydl.download([self.url])

				for file in os.listdir():
					if file.endswith('.webm'):
						os.remove(file)

				self.pb.destroy()
				messagebox.showinfo('SaveFromYT', 'Successfully Downloaded Mp3')
			except:
				messagebox.showinfo('SaveFromYT', "Can't connect with internet")

	def download_hook(self, d):
		if d['status'] == 'downloading':
			p = d['_percent_str']
			p = float(p.replace('%','').replace(' ',''))
			self.pb['value'] = round(p)
			self.update()

	def go_back(self):
		self.info_frame.destroy()
		self.video_frame.destroy()
		self.audio_frame.destroy()
		self.back_frame.destroy()

		self.draw_main_frame()

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('450x320')
	root.title('SaveFromYT')
	root.resizable(0,0)

	youtube_icon = PhotoImage(file='icons/youtube.png')
	back_icon = PhotoImage(file='icons/back.png')
	search_icon = PhotoImage(file='icons/search.png')

	app = Application(master=root)
	app.mainloop()