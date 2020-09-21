from matplotlib.figure import Figure 
import numpy as np

def get_plot(m1, m2, func):
	v1 = m1 * np.pi / 180
	v2 = m2 * np.pi / 180

	figure = Figure(figsize=(6, 4), dpi=100)
	plot = figure.add_subplot(111)

	x = np.linspace(v1, v2, 1000)

	if func == 'sin':
		y = np.sin(x)
		plot.plot(x, y)
	elif func == 'cos':
		y = np.cos(x)
		plot.plot(x, y)
	elif func == 'tan':
		y = np.tan(x)
		y[:-1][np.diff(y) < 0] = np.nan
		plot.plot(x, y)
		plot.set_ylim(-10,10)
	elif func == 'cosec':
		y = 1 / np.sin(x)
		plot.plot(x, y)
		plot.set_ylim(-10,10)
	elif func == 'sec':
		y = 1 / np.cos(x)
		plot.plot(x, y)
		plot.set_ylim(-10,10)
	elif func == 'cot':
		y = 1 / np.tan(x)
		y[:-1][np.diff(y) > 0] = np.nan
		plot.plot(x, y)
		plot.set_ylim(-10,10)

	plot.set_title(f'Graph of {func}(x)')
	plot.set_xlabel(f'x values from {m1} to {m2}')
	plot.set_ylabel('y(x)')

	return figure