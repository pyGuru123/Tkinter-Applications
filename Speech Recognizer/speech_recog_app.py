# Speech Recognizer

# Importing libraries --------------------------------------------------------

# pip install SpeechRecognition
# pip install pypiwin32

import os
import tkinter as tk 
from tkinter import filedialog
from tkinter import messagebox
import speech_recognition as sr  
from win32com.client import constants, Dispatch 

# Setup ----------------------------------------------------------------------

cwd = os.getcwd()

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)

speaker = Dispatch("SAPI.SpVoice")

# Application Class ------------------------------------------------------------

class Application(tk.Frame):
	def __init__(self, master=None): 
		super().__init__(master=master)
		self.master = master 
		self.pack()
		self.main_frame()

	def main_frame(self):
		self.delete_frame()

		self.frame1 = tk.Frame(self)
		self.frame1.config(width=400, height=100)
		self.frame1.grid(row=0, column=0, columnspan=2)

		self.label1 = tk.Label(self.frame1)
		self.label1['text'] = 'Speech Recognition App'
		self.label1.grid(row=0, column=0, pady=30)

		self.label2 = tk.Label(self.frame1)
		self.label2['text'] = 'Requires an Active Internet Connection'
		self.label2.grid(row=1, column=0, pady=10, padx=100)

		self.speech2text = tk.Button(self, bg='green', fg='white')
		self.speech2text['text'] = 'Speech to Text'
		self.speech2text['command'] = self.speech2text_frame
		self.speech2text.grid(row=1, column=0, pady=80, padx=60)

		self.text2speech = tk.Button(self, bg='green', fg='white')
		self.text2speech['text'] = 'Text to Speech'
		self.text2speech['command'] = self.text2speech_frame
		self.text2speech.grid(row=1, column=1, pady=60, padx=60)

	def delete_frame(self):
		for widgets in self.winfo_children():
			widgets.destroy()

	def speech2text_frame(self):
		self.delete_frame()

		self.listen = tk.Button(self, bg='DeepSkyBlue2', fg='white')
		self.listen['text'] = 'Listen'
		self.listen['command'] = self.recognize_audio
		self.listen.grid(row=0, column=0, pady=40)

		self.back = tk.Button(self, bg='red', fg='white')
		self.back['text'] = ' <- '
		self.back['command'] = self.main_frame
		self.back.grid(row=0, column=2)

		self.text = tk.Text(self)
		self.text.configure(width=48, height=10)
		self.text.grid(row=1, column=0, columnspan=3)

	def text2speech_frame(self):
		self.delete_frame()

		self.scroll = tk.Scrollbar(self, orient = tk.VERTICAL)
		self.scroll.grid(row=0, column=4, sticky='ns', padx=0)

		self.text = tk.Text(self)
		self.text.configure(width=44, height=12)
		self.text.grid(row=0, column=0, columnspan=3)

		self.text.config(yscrollcommand=self.scroll.set)
		self.scroll.config(command = self.text.yview)

		self.get_audio = tk.Button(self, bg='DeepSkyBlue2', fg='white')
		self.get_audio['text'] = 'Get Audio'
		self.get_audio['command'] = self.convert_text2speech
		self.get_audio.grid(row=1, column=0, pady=50)

		self.read_file = tk.Button(self, bg='DeepSkyBlue2', fg='white')
		self.read_file['text'] = 'Read file'
		self.read_file['command'] = self.read_file_text
		self.read_file.grid(row=1, column=1)

		self.clear = tk.Button(self, bg='DeepSkyBlue2', fg='white')
		self.clear['text'] = 'Clear'
		self.clear['command'] = self.clear_textbox
		self.clear.grid(row=1, column=2)

		self.back = tk.Button(self, bg='red', fg='white')
		self.back['text'] = ' <- '
		self.back['command'] = self.main_frame
		self.back.grid(row=1, column=3)

	def recognize_audio(self):
		self.clear_textbox()
		try:
			with mic as source:
				audio = r.listen(source)

			msg = r.recognize_google(audio)
			self.text.insert('1.0', msg)
		except:
			self.text.insert('1.0', 'No internet connection')

	def convert_text2speech(self):
		self.msg = self.text.get(1.0, tk.END)
		if self.msg.strip('\n') != '':
			speaker.speak(self.msg)
		else:
			speaker.speak('Write some message first')

	def read_file_text(self):
		self.filename = filedialog.askopenfilename(initialdir=cwd)

		if (self.filename == '') or (not self.filename.endswith('.txt')):
			messagebox.showerror('Cant load file', 'Choose a text file to read')
		else:
			with open(self.filename) as f:
				text = f.read()
				self.clear_textbox()
				self.text.insert('1.0', text)

	def clear_textbox(self):
		self.text.delete(1.0, tk.END)

# Main App -----------------------------------------------------------------------

root = tk.Tk()
root.geometry('400x300')
root.wm_title('Speech Recognizer')

app = Application(master=root)
app['bg'] = 'slate gray'
app.mainloop()