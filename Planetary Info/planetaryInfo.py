# importing required libraries --------------------------------------------------

# pip install requests

import time
import requests
import tkinter as tk
import tkinter.messagebox


# Defining functions ------------------------------------------------------------

def planetary_data(url):
	r = requests.get(url)
	data = r.json()
	time.sleep(1)

	if data['moons'] != None:
		all_moons = []
    
		num_moons = len(data['moons'])
	else:
		num_moons = 0

	semi_major_axis = data['semimajorAxis']
	perihelion = data['perihelion']
	aphelion = data['aphelion']

	mass = data['mass']['massValue']
	mexp = data['mass']['massExponent']
	volume = data['vol']['volValue']
	vexp = data['vol']['volExponent']
	density = data['density']
	gravity = data['gravity']
	escape = data['escape']

	mean = data['meanRadius']
	equa = data['equaRadius']
	polar = data['polarRadius']

	ar = data['aroundPlanet']
	if ar == None:
		around = None
	else:
		around = ar['planet']
	rot = data['sideralRotation']
	rev = data['sideralOrbit']

	disBy = data['discoveredBy']
	date = data['discoveryDate']


	return [num_moons, semi_major_axis, perihelion, aphelion, (mass, mexp), 
			(volume, vexp), density, gravity, escape, (mean, equa, polar), 
			(around, rot, rev), (disBy, date)]

def planetDef(url):
	r = requests.get(url)
	data = r.json()
	if len(data) != 0:
		return data['definition']
	else:
		return 'No information on this term'

# Application Class ----------------------------------------------------------------

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		self.search_widgets()
		self.data_widgets()

	def search_widgets(self):
		self.query = tk.StringVar(self)
		self.search_box = tk.Entry(self, width=60)
		self.search_box['textvariable'] = self.query
		self.search_box.grid(row=0, column=1, columnspan=3, pady=5)

		self.search = tk.Button(self, bg='green', fg='white', font=10)
		self.search['text'] = 'Search'
		self.search['command'] = self.get_data
		self.search.grid(row=0, column=4, pady=5)


	def data_widgets(self):
		self.nameLabel = tk.Label(self)
		self.nameLabel['text'] = 'Name'
		self.nameLabel.grid(row=2, column=1, pady=10)
		self.nameValue = tk.StringVar()
		self.name = tk.Entry(self)
		self.name['textvariable'] = self.nameValue
		self.name.grid(row=2, column=2, pady=10)

		self.moonLabel = tk.Label(self)
		self.moonLabel['text'] = 'Number of Moons'
		self.moonLabel.grid(row=2, column=3, padx=5)
		self.moonValue = tk.StringVar()
		self.moon = tk.Entry(self)
		self.moon['textvariable'] = self.moonValue
		self.moon.grid(row=2, column=4)

		self.semiLabel = tk.Label(self)
		self.semiLabel['text'] = 'Semi Major Axis (km)'
		self.semiLabel.grid(row=5, column=4)
		self.semiValue = tk.StringVar()
		self.semi = tk.Entry(self)
		self.semi['textvariable'] = self.semiValue
		self.semi.grid(row=5, column=5)

		self.periLabel = tk.Label(self)
		self.periLabel['text'] = 'Perihelion (km)'
		self.periLabel.grid(row=6, column=4)
		self.periValue = tk.StringVar()
		self.peri = tk.Entry(self)
		self.peri['textvariable'] = self.periValue
		self.peri.grid(row=6, column=5)

		self.aphiLabel = tk.Label(self)
		self.aphiLabel['text'] = 'Aphelion (km)'
		self.aphiLabel.grid(row=7, column=4)
		self.aphiValue = tk.StringVar()
		self.aphi = tk.Entry(self)
		self.aphi['textvariable'] = self.aphiValue
		self.aphi.grid(row=7, column=5)

		self.massLabel = tk.Label(self)
		self.massLabel['text'] = 'Mass (kg)'
		self.massLabel.grid(row=4, column=0, pady=5)
		self.massValue = tk.StringVar()
		self.mass = tk.Entry(self)
		self.mass['textvariable'] = self.massValue
		self.mass.grid(row=4, column=1, pady=5)

		self.volLabel = tk.Label(self)
		self.volLabel['text'] = 'Volume (kg/km**3)'
		self.volLabel.grid(row=5, column=0)
		self.volValue = tk.StringVar()
		self.vol = tk.Entry(self)
		self.vol['textvariable'] = self.volValue
		self.vol.grid(row=5, column=1)

		self.densityLabel = tk.Label(self)
		self.densityLabel['text'] = 'Density (g/cm3)'
		self.densityLabel.grid(row=6, column=0)
		self.densityValue = tk.StringVar()
		self.density = tk.Entry(self)
		self.density['textvariable'] = self.densityValue
		self.density.grid(row=6, column=1)

		self.gravityLabel = tk.Label(self)
		self.gravityLabel['text'] = 'Gravity (m/s-2)'
		self.gravityLabel.grid(row=7, column=0)
		self.gravityValue = tk.StringVar()
		self.gravity = tk.Entry(self)
		self.gravity['textvariable'] = self.gravityValue
		self.gravity.grid(row=7, column=1)

		self.escapeLabel = tk.Label(self)
		self.escapeLabel['text'] = 'Escape vel. (m/s)'
		self.escapeLabel.grid(row=8, column=0)
		self.escapeValue = tk.StringVar()
		self.escape = tk.Entry(self)
		self.escape['textvariable'] = self.escapeValue
		self.escape.grid(row=8, column=1)

		self.meanRLabel = tk.Label(self)
		self.meanRLabel['text'] = 'Mean Radius (km)'
		self.meanRLabel.grid(row=9, column=4)
		self.meanRValue = tk.StringVar()
		self.meanR = tk.Entry(self)
		self.meanR['textvariable'] = self.meanRValue
		self.meanR.grid(row=9, column=5)

		self.equaRLabel = tk.Label(self)
		self.equaRLabel['text'] = 'Equa. Radius (km)'
		self.equaRLabel.grid(row=10, column=4)
		self.equaRValue = tk.StringVar()
		self.equaR = tk.Entry(self)
		self.equaR['textvariable'] = self.equaRValue
		self.equaR.grid(row=10, column=5)

		self.polarRLabel = tk.Label(self)
		self.polarRLabel['text'] = 'Polar Radius (km)'
		self.polarRLabel.grid(row=11, column=4)
		self.polarRValue = tk.StringVar()
		self.polarR = tk.Entry(self)
		self.polarR['textvariable'] = self.polarRValue
		self.polarR.grid(row=11, column=5)

		self.aroundLabel = tk.Label(self)
		self.aroundLabel['text'] = 'Around Planet'
		self.aroundLabel.grid(row=10, column=0)
		self.aroundValue = tk.StringVar()
		self.around = tk.Entry(self)
		self.around['textvariable'] = self.aroundValue
		self.around.grid(row=10, column=1)

		self.rotLabel = tk.Label(self)
		self.rotLabel['text'] = 'Rotation (hrs)'
		self.rotLabel.grid(row=11, column=0)
		self.rotValue = tk.StringVar()
		self.rot = tk.Entry(self)
		self.rot['textvariable'] = self.rotValue
		self.rot.grid(row=11, column=1)

		self.revLabel = tk.Label(self)
		self.revLabel['text'] = 'Revolution (days)'
		self.revLabel.grid(row=12, column=0)
		self.revValue = tk.StringVar()
		self.rev = tk.Entry(self)
		self.rev['textvariable'] = self.revValue
		self.rev.grid(row=12, column=1)

		self.disLabel = tk.Label(self)
		self.disLabel['text'] = 'Discovered by'
		self.disLabel.grid(row=14, column=0, pady=5)
		self.disValue = tk.StringVar()
		self.dis = tk.Entry(self)
		self.dis['textvariable'] = self.disValue
		self.dis.grid(row=14, column=1)

		self.dateLabel = tk.Label(self)
		self.dateLabel['text'] = 'Discovery Date'
		self.dateLabel.grid(row=15, column=0)
		self.dateValue = tk.StringVar()
		self.date = tk.Entry(self)
		self.date['textvariable'] = self.dateValue
		self.date.grid(row=15, column=1)

		self.text = tk.Text(self, height=9, width=53)
		self.text.insert(tk.END, '\nEnter planet or moon name to get related data')
		self.text.insert(tk.END, '\nInternet connection is required')
		self.text.grid(row=14, column=2, columnspan=4, rowspan=6)

	def get_data(self):
		self.id_ = self.query.get()
		if self.id_ == '':
			tk.messagebox.showerror('Cant search', 'Enter planet/moon name first')
		else:
			self.url1 = f'https://api.le-systeme-solaire.net/rest/bodies/{self.id_}'
			self.url2 = f'http://hubblesite.org/api/v3/glossary/{self.id_}'
			try:
				self.data = planetary_data(self.url1)
				self.definition = planetDef(self.url2)
				self.nameValue.set(self.id_)
				self.moonValue.set(self.data[0])
				self.semiValue.set(self.data[1])
				self.periValue.set(self.data[2])
				self.aphiValue.set(self.data[3])
				self.massValue.set(f'{self.data[4][0]} * 10 **{self.data[4][1]}')
				self.volValue.set(f'{self.data[5][0]} *  10 ** {self.data[5][1]} ')
				self.densityValue.set(self.data[6])
				self.gravityValue.set(self.data[7])
				self.escapeValue.set(self.data[8])
				self.meanRValue.set(self.data[9][0])
				self.equaRValue.set(self.data[9][1])
				self.polarRValue.set(self.data[9][2])
				self.aroundValue.set(self.data[10][0])
				self.rotValue.set(self.data[10][1])
				self.revValue.set(self.data[10][2])
				self.disValue.set(self.data[11][0])
				self.dateValue.set(self.data[11][1])
				self.text.delete('1.0',tk.END)
				self.text.insert(tk.END, self.definition)
			except:
				tk.messagebox.showerror('Cant retrieve data', 'No internet access')

# Main app ------------------------------------------------------------------------

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('700x500')
	root.wm_title('Planetary Info')

	app = Application(master=root)
	app.mainloop()