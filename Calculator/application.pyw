import re
import tkinter as tk
from math import sqrt

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.pack()

		self.input = '0'
		self.draw_frame()

	def create_button(self, text, color, command, r, c, cspan=1, w=8):
		self.button = tk.Button(self, bg=color, fg='white')
		self.button['text'] = text
		self.button['command'] = command
		self.button.config(height=2, width=w)
		self.button.grid(row=r, column=c, columnspan=cspan, pady=4)

		return self.button

	def draw_frame(self):
		self.label = tk.Label(self, font=("Helvetica", 16), bg='gray30', fg='white', anchor='se') 
		self.label['text'] = '0'
		self.label.configure(width=23, height=5)
		self.label.grid(row=0, column=0, columnspan=4, pady=10)

		self.ce = self.create_button('CE', 'red2', self.clear, 1, 0)
		self.back = self.create_button(u'\u232b', 'gray20', self.back, 1, 1)
		self.mod = self.create_button('%', 'gray20', lambda : self.get('%'), 1, 2)
		self.div = self.create_button('/', 'gray20', lambda : self.get('/'), 1, 3)

		self.seven = self.create_button('7', 'gray20', lambda : self.get('7'), 2, 0)
		self.eight = self.create_button('8', 'gray20', lambda : self.get('8'), 2, 1)
		self.nine = self.create_button('9', 'gray20', lambda : self.get('9'), 2, 2)
		self.mul = self.create_button('X', 'gray20', lambda : self.get('*'), 2, 3)

		self.four = self.create_button('4', 'gray20', lambda : self.get('4'), 3, 0)
		self.five = self.create_button('5', 'gray20', lambda : self.get('5'), 3, 1)
		self.six = self.create_button('6', 'gray20', lambda : self.get('6'), 3, 2)
		self.minus = self.create_button('-', 'gray20', lambda : self.get('-'), 3, 3)

		self.one = self.create_button('3', 'gray20', lambda : self.get('3'), 4, 0)
		self.two = self.create_button('2', 'gray20', lambda : self.get('2'), 4, 1)
		self.three = self.create_button('1', 'gray20', lambda : self.get('1'), 4, 2)
		self.plus = self.create_button('+', 'gray20', lambda : self.get('+'), 4, 3)

		self.root = self.create_button('√', 'gray20', lambda : self.get('√'), 5, 0)
		self.zero = self.create_button('0', 'gray20', lambda : self.get('0'), 5, 1)
		self.dot = self.create_button('.', 'gray20', lambda : self.get('.'), 5, 2)
		self.equal = self.create_button('=', 'gray20', self.output, 5, 3)

	def get(self, value):
		self.input += str(value)
		self.ops = ['+','-','*','/','%', '√']

		if self.input[-1] in self.ops and self.input[-2] in self.ops:
			self.input = str(self.input[:-2] + self.input[-1])
		if self.input[0] == '0': 
			self.input = self.input[1:]
		if self.input[0] in self.ops:
			self.input = self.input[1:]
			self.input = '0' + self.input

		self.label['text'] = self.input

	def clear(self):
		self.input = '0'
		self.label['text'] = self.input

	def back(self):
		self.text = self.input
		if len(self.input) == 1:
			self.clear()
		else:
			self.input = self.text[:-1]
			self.label['text'] = self.input

	def output(self):
		root_ = re.compile(r'√\d+')
		all_roots = re.findall(root_, self.input)
		if all_roots:
			for num in all_roots:
				calc = sqrt(int(num.lstrip('√')))
				self.input = re.sub(num, '*'+str(round(calc,3)), self.input)

				if self.input[0] == '*' :
					self.input = self.input[1:]

		self.out = str(round(eval(self.input), 5))
		self.label['text'] = self.out
		self.input = self.out

# *********************************************************************************

root = tk.Tk()
root.geometry('300x400')
root.wm_title('Calculator')

app = Application(master=root)
app.mainloop()