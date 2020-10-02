import requests
import subprocess
from urllib.parse import quote

import tkinter as tk
from tkinter import PhotoImage

FORMATS = [("PNG", '.png'), ("JPG", '.jpg'), ("GIF", '.gif')]

class LatexGenerator(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.pack()

		self.draw_frames()

	def draw_frames(self):
		self.header = tk.Label(self, text='Latex Equation Generator',
								font=('Lemon Regular', 13), fg='OrangeRed3')
		self.header.grid(row=0, column=1, columnspan=5, pady=5)

		self.output = tk.Text(self)
		self.output.insert(tk.END, '\n\n\n\n\tWrite your equation to generate png')
		self.output.configure(width=55, height=12, state='disabled')
		self.output.grid(row=1, column=0, columnspan=7, pady=10)

		self.format = tk.StringVar()
		self.format.set('.png')
		self.radios = [self.create_radios(format) for format in FORMATS]
		r = 2
		for radio in self.radios:
			radio.grid(row=r, column=0)
			r += 1

		self.help = tk.Button(self, text='LATEX Help', bg='dodger blue')
		self.help.configure(width=11)
		self.help['command'] = self.get_help
		self.help.grid(row=2, column=6)

		self.input = tk.Text(self)
		self.input.configure(width=35, height=2)
		self.input.grid(row=3, column=1, columnspan=5, pady=(10,2))

		self.send = tk.Button(self, text='Generate\nLATEX', bg='green', fg='white')
		self.send.configure(width=11)
		self.send['command'] = self.generate_latex
		self.send.grid(row=3, column=6, pady=(10,2))

	def create_radios(self, option):
		text, value = option
		radio = tk.Radiobutton(self, text=text, value=value, variable=self.format)
		return radio

	def generate_latex(self):
		fmt = self.format.get()
		filename = 'image' + fmt

		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

		formula = self.input.get('1.0', tk.END).strip('\n')
		if len(formula) > 0:
			formula = quote(formula)

			base_url = 'https://chart.apis.google.com/chart?cht=tx&chs=428x35&chf=bg,s,FFFFFF00&chl='
			url = base_url + formula

			r = requests.get(url, headers=headers)
			with open(filename, 'wb') as f:
				f.write(r.content)

			self.img = tk.PhotoImage(file=filename)
			self.output.configure(state='normal')
			self.output.delete(1.0, tk.END)
			self.output.insert(tk.END, '\n\n\n\n')
			self.output.image_create(tk.END, image = self.img)
			self.output.configure(state='disabled')

	def get_help(self):
		file = 'files/LaTeX - Basic Code.pdf'
		subprocess.Popen([file],shell=True)

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('510x370')
	root.title('Latex Equation Generator')
	root.iconbitmap('icons/icon.ico')

	app = LatexGenerator(master=root)
	app.mainloop()