from os import system
from numpy import min, max, mean, ndarray, asarray, asmatrix, arange
from numpy.random import randint
from string import rstrip

class Settings(object):
	tmp_dir = '/tmp/'
	command = 'pdflatex -halt-on-error -interaction nonstopmode {0}'
#	command = 'pdflatex -halt-on-error -interaction batchmode {0} > /dev/null'
	preamble = \
		'\\usepackage[utf8]{inputenc}\n' + \
		'\\usepackage{amsmath}\n' + \
		'\\usepackage{amssymb}\n' + \
		'\\usepackage{pgfplots}\n'



class Figure(object):
	# currently active figure
	_figures = {}
	_cf = None
	_session = randint(1E8)

	@staticmethod
	def gcf():
		if not Figure._cf:
			Figure()
		return Figure._cf



	def __new__(cls, idx=None, *args, **kwargs):
		if idx in Figure._figures:
			# figure with specified ID already exists
			return Figure._figures[idx]
		else:
			# create new figure
			fig = object.__new__(cls, idx, *args, **kwargs)
			fig._idx = min_free(Figure._figures.keys())

			# store figure
			Figure._figures[fig._idx] = fig

			return fig




	def __init__(self, *args, **kwargs):
		self.axes = []

		# width and height of the figure
		self.width = None
		self.height = None

		# space around axes
		self.margin = kwargs.get('margin', 2.)

		# move focus to this figure
		Figure._cf = self



	def render(self):
		"""
		Returns the LaTeX code for this figure.

		@rtype: string
		@return: LaTeX code for this figure
		"""

		# figure width and height
		width, height = self.width, self.height

		if self.axes:
			if not width:
				width = self.margin * 2. \
					+ max([ax.left + ax.width for ax in self.axes])
			if not height:
				height = self.margin * 2. \
					+ max([ax.top + ax.height for ax in self.axes])
		else:
			if not width:
				width = self.margin * 2. + 1.
			if not height:
				height = self.margin * 2. + 1.

		tex = \
			'\\documentclass{article}\n' + \
			'\n' + \
			Settings.preamble + \
			'\n' + \
			'\\usepackage[\n' + \
			'\tmargin=0cm,\n' + \
			'\tpaperwidth={0}cm,\n'.format(width) + \
			'\tpaperheight={0}cm]{{geometry}}\n'.format(height) + \
			'\n' + \
			'\\begin{document}\n' + \
			'\t\\thispagestyle{empty}\n' + \
			'\n'
		if self.axes:
			tex += \
				'\t\\begin{figure}\n' + \
				'\t\t\\centering\n' + \
				'\t\t\\begin{tikzpicture}\n'
			for ax in self.axes:
				tex += indent(ax.render(), 3)
			tex += \
				'\t\t\\end{tikzpicture}\n' + \
				'\t\\end{figure}\n'
		else:
			tex += '\t\\mbox{}\n'
		tex += \
			'\\end{document}'

		return tex



	def draw(self):
		tex_file = Settings.tmp_dir + 'pgf_{0}_{1}.tex'.format(Figure._session, self._idx)
		pdf_file = Settings.tmp_dir + 'pgf_{0}_{1}.pdf'.format(Figure._session, self._idx)
		tex_command = Settings.command.format('-output-directory {0} {1}')
		tex_command = tex_command.format(Settings.tmp_dir, tex_file)
		pdf_command = 'open {0}'.format(pdf_file)

		# write LaTeX file
		with open(tex_file, 'w') as handle:
			handle.write(self.render())

		# compile LaTeX to PDF
		if system(tex_command):
			raise RuntimeError('Compiling LaTeX to PDF failed. Sorry.')

		# open PDF file
		if system(pdf_command):
			raise RuntimeError('Can\'t open file {0}.'.format(pdf_file))



class Axis(object):
	_ca = None

	@staticmethod
	def gca():
		if not Axis._ca:
			Axis()
		return Axis._ca



	def __init__(self, fig=None, *args, **kwargs):
		# position of axis
		self.top = 0.
		self.left = 0.

		# width and height of axis
		self.width = 8.
		self.height = 7.

		# parent figure
		self.figure = fig

		# plots contained in this axis
		self.plots = []

		# title above this axis
		self.title = kwargs.get('title', '')

		# axis labels
		self.xlabel = kwargs.get('xlabel', '')
		self.ylabel = kwargs.get('ylabel', '')

		# axis boundaries
		self.xmin = kwargs.get('xmin', None)
		self.xmax = kwargs.get('xmax', None)
		self.ymin = kwargs.get('ymin', None)
		self.ymax = kwargs.get('ymax', None)

		# controls aspect ratio
		self.equal = kwargs.get('equal', False)

		# grid lines
		self.grid = kwargs.get('grid', False)

		# add axis to figure
		if not self.figure:
			self.figure = Figure.gcf()
		self.figure.axes.append(self)

		Axis._ca = self



	def render(self):
		"""
		Returns the LaTeX code for this axis.

		@rtype: string
		@return: LaTeX code for this axis
		"""

		options = [
			'at={{({0}, {1})}}'.format(self.left, self.top),
			'scale only axis',
			'width={0}cm'.format(self.width),
			'height={0}cm'.format(self.height)]

		properties = [
			'title',
			'xmin',
			'xmax',
			'ymin',
			'ymax',
			'xlabel',
			'ylabel']

		for prop in properties:
			if self.__dict__.get(prop, None) not in ['', None, False]:
				options.append('{0}={{{1}}}'.format(prop, self.__dict__[prop]))

		if self.xlabel:
			options.append('xlabel near ticks')
		if self.ylabel:
			options.append('ylabel near ticks')
		if self.equal:
			options.append('axis equal=true')
		if self.grid:
			options.append('grid=major')

		tex = '\\begin{axis}[\n' + indent(',\n'.join(options), 2) + '\n\t]\n'
		for plot in self.plots:
			tex += indent(plot.render())
		tex += '\\end{axis}\n'

		return tex



class Plot(object):
	def __init__(self, *args, **kwargs):
		# add plot to axis
		self.axis = kwargs.get('axis', Axis.gca())
		self.axis.plots.append(self)

		self.format_string = ''.join([arg
			for arg in args if isinstance(arg, str)])

		values = [arg for arg in args if not isinstance(arg, str)]

		if len(values) < 1:
			self.xvalues = asarray([])
			self.yvalues = asarray([])

		elif len(values) < 2:
			self.yvalues = asarray(values[0]).flatten()
			self.xvalues = arange(1, len(self.yvalues) + 1)

		else:
			self.xvalues = asarray(values[0]).flatten()
			self.yvalues = asarray(values[1]).flatten()



	def render(self):
		color = 'blue'
		linestyle = 'solid'
		marker = 'no marks'
		marker_options = []

		# determine color
		if 'r' in self.format_string:
			color = 'red'
		elif 'g' in self.format_string:
			color = 'green'
		elif 'b' in self.format_string:
			color = 'blue'
		elif 'c' in self.format_string:
			color = 'cyan'
		elif 'm' in self.format_string:
			color = 'magenta'
		elif 'y' in self.format_string:
			color = 'yellow'
		elif 'k' in self.format_string:
			color = 'black'
		elif 'w' in self.format_string:
			color = 'white'

		# determine marker style
		if '.' in self.format_string:
			marker = 'mark=*'
			marker_options.append('solid')
			marker_options.append('fill={0}'.format(color))
		elif 'o' in self.format_string:
			marker = 'mark=o'
			marker_options.append('solid')
		elif '+' in self.format_string:
			marker = '+'
		elif '*' in self.format_string:
			marker = 'mark=asterisk'
		elif 'x' in self.format_string:
			marker = 'mark=x'
		elif 'd' in self.format_string:
			marker = 'mark=diamond'
		elif '^' in self.format_string:
			marker = 'mark=triangle'
		elif 'p' in self.format_string:
			marker = 'mark=pentagon'

		# determine line style
		if '--' in self.format_string:
			linestyle = 'dashed'
		elif '-' in self.format_string:
			linestyle = 'solid'
		elif ':' in self.format_string:
			linestyle = 'densely dotted'

		if (marker != 'no marks') \
			and '-' not in self.format_string \
			and ':' not in self.format_string:
			linestyle = 'only marks'

		if marker_options:
			marker += ', mark options={' + ', '.join(marker_options) + '}'

		# produce LaTeX code
		tex = '\\addplot+[{0}] coordinates {{\n'.format(
			'{0}, {1}, {2}'.format(color, linestyle, marker))

		for x, y in zip(self.xvalues, self.yvalues):
			tex += '\t({0}, {1})\n'.format(x, y)

		tex += '};\n'

		return tex




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



def indent(text, times=1, ind='\t'):
	"""
	Indent text with multiple lines.

	@type  text: string
	@param text: some text

	@type  times: integer
	@param times: number of indentations

	@type  ind: string
	@param ind: string inserted at the beginning of each line
	"""

	if times > 1:
		text = indent(text, times - 1)
	return '\n'.join([rstrip(ind + line) for line in text.split('\n')])



def min_free(indices):
	if not indices:
		return 0
	return min(list(set(range(max(indices) + 2)).difference(indices)))
