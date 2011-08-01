from os import system
from numpy import min, max, mean, ndarray, asarray, asmatrix, arange
from numpy.random import randint
from string import rstrip

class Settings(object):
	tmp_dir = '/tmp/'
#	command = 'pdflatex -halt-on-error -interaction nonstopmode {0}'
	command = 'pdflatex -halt-on-error -interaction batchmode {0} > /dev/null'
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

		# tick positions
		self.xtick = kwargs.get('xtick', None)
		self.ytick = kwargs.get('ytick', None)

		# tick labels
		self.xticklabels = kwargs.get('xticklabels', None)
		self.yticklabels = kwargs.get('yticklabels', None)

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
		if self.xtick:
			options.append('xtick={{{0}}}'.format(
				','.join(str(t) for t in self.xtick)))
		if self.ytick:
			options.append('ytick={{{0}}}'.format(
				','.join(str(t) for t in self.ytick)))
		if self.xticklabels:
			options.append('xticklabels={{{0}}}'.format(
				','.join(str(t) for t in self.xticklabels)))
		if self.yticklabels:
			options.append('yticklabels={{{0}}}'.format(
				','.join(str(t) for t in self.yticklabels)))

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

		# separate data from formatting information
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

		# marker style
		self.marker = kwargs.get('marker', 'no marks')
		self.marker_size = kwargs.get('marker_size', 1)
		self.marker_edge_color = kwargs.get('marker_edge_color', None)
		self.marker_face_color = kwargs.get('marker_face_color', None)

		# opacity
		self.opacity = kwargs.get('opacity', None)
		self.fill_opacity = kwargs.get('fill_opacity', None)



	def render(self):
		color = 'blue'
		linestyle = 'solid'
		marker = 'mark={0}'.format(self.marker)
		marker_options = ['scale={0}'.format(self.marker_size)]

		if self.marker_edge_color:
			marker_options.append('{0}'.format(self.marker_edge_color))
		if self.marker_face_color:
			marker_options.append('fill={0}'.format(self.marker_face_color))

		if self.fill_opacity is not None:
			marker_options.append('fill opacity={0}'.format(self.fill_opacity))
		elif self.opacity is not None:
			marker_options.append('fill opacity={0}'.format(self.opacity))

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
			if not self.marker_face_color:
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

		options = [color, linestyle, marker]
		if self.opacity is not None:
			options.append('opacity={0}'.format(self.opacity))

		# produce LaTeX code
		tex = '\\addplot+[{0}] coordinates {{\n'.format(
			', '.join(options))
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
