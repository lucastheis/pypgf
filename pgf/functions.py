from axis import Axis
from figure import Figure
from settings import Settings
from plot import Plot
from numpy import asmatrix

def gcf():
	"""
	Return currently active figure.
	"""
	return Figure.gcf()


def gca():
	"""
	Return currently active axis.
	"""

	return Axis.gca()


def draw():
	gcf().draw()


def figure(idx=None):
	return Figure(idx)


def plot(*args, **kwargs):
	values = [asmatrix(arg) for arg in args if not isinstance(arg, str)]
	format_string = ''.join([arg for arg in args if isinstance(arg, str)])

	# if arguments contain multiple rows, create multiple plots
	if (len(values) > 1) and (values[1].shape[0] > 1) and (values[0].shape[0] == 1):
		return [plot(format_string, values[0], *[value[i] for value in values[1:]], **kwargs)
			for i in range(len(values[0]))]

	elif (len(values) > 0) and (values[0].shape[0] > 1):
		return [plot(format_string, *[value[i] for value in values], **kwargs)
			for i in range(len(values[0]))]

	return Plot(*args, **kwargs)


def title(title):
	gca().title = title


def xlabel(xlabel):
	gca().xlabel = xlabel


def ylabel(ylabel):
	gca().ylabel = ylabel


def xtick(xtick):
	gca().xtick = xtick


def ytick(ytick):
	gca().ytick = ytick


def xticklabels(xticklabels):
	gca().xticklabels = xticklabels


def yticklabels(yticklabels):
	gca().yticklabels = yticklabels


def axis(*args):
	if len(args) < 1:
		return gca()

	if len(args) < 4:
		if isinstance(args[0], str):
			ax = gca()

			if args[0] == 'equal':
				gca().equal = True
			if args[0] == 'square':
				ax.width = ax.height = mean([gca().width, gca().height])

		elif isinstance(args[0], list) or isinstance(args[0], ndarray):
			gca().xmin, gca().xmax, gca().ymin, gca().ymax = args[0]


def grid(value=None):
	if value == 'off':
		gca().grid = False
	elif value == 'on':
		gca().grid = True
	else:
		gca().grid = not gca().grid
