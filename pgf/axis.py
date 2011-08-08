from utils import indent
from figure import Figure

class Axis(object):
	"""
	Manages axis properties.

	@type at: tuple
	@ivar at: axis position

	@type width: float
	@ivar width: axis width

	@type height: float
	@ivar height: axis height

	@type title: string
	@ivar title: title above axis

	@type xlabel: string
	@ivar xlabel: label at the x-axis

	@type ylabel: string
	@ivar ylabel: label at the y-axis

	@type xmin: float/None
	@ivar xmin: minimum of x-axis

	@type xmax: float/None
	@ivar xmax: maximum of x-axis

	@type ymin: float/None
	@ivar ymin: minimum of y-axis

	@type ymax: float/None
	@ivar ymax: maximum of y-axis

	@type xtick: list/None
	@ivar xtick: location of ticks at x-axis

	@type ytick: list/None
	@ivar ytick: location of ticks at y-axis

	@type xticklabels: list/None
	@ivar xticklabels: labeling of ticks

	@type yticklabels: list/None
	@ivar yticklabels: labeling of ticks

	@type equal: boolean/None
	@ivar equal: forces units on all axis to have equal lengths

	@type grid: boolean/None
	@ivar grid: enables major grid

	@type pgf_options: list
	@ivar pgf_options: custom PGFPlots axis options

	@type children: list
	@ivar children: list of plots contained in this axis
	"""

	_ca = None

	@staticmethod
	def gca():
		"""
		Returns the currently active axis.
		"""

		if not Axis._ca:
			Axis()
		return Axis._ca


	def __init__(self, fig=None, *args, **kwargs):
		"""
		Initializes axis properties.
		"""

		self.legend = None

		# axis position
		self.at = [0., 0.]

		# width and height of axis
		self.width = 8.
		self.height = 7.

		# parent figure
		self.figure = fig

		# plots contained in this axis
		self.children = []

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
		self.equal = kwargs.get('equal', None)

		# grid lines
		self.grid = kwargs.get('grid', None)

		# add axis to figure
		if not self.figure:
			self.figure = Figure.gcf()
		self.figure.axes.append(self)

		# custom axis options
		self.pgf_options = kwargs.get('pgf_options', [])

		Axis._ca = self


	def render(self):
		"""
		Produces the LaTeX code for this axis.

		@rtype: string
		@return: LaTeX code for this axis
		"""

		options = [
			'at={{({0}, {1})}}'.format(self.at[0], self.at[1]),
			'scale only axis',
			'width={0}cm'.format(self.width),
			'height={0}cm'.format(self.height)]
		options.extend(self.pgf_options)

		properties = [
			'title',
			'xmin',
			'xmax',
			'ymin',
			'ymax',
			'xlabel',
			'ylabel']

		for prop in properties:
			if self.__dict__.get(prop, None) not in ['', None]:
				options.append('{0}={{{1}}}'.format(prop, self.__dict__[prop]))

		if self.legend:
			options.append(self.legend.render())
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

		tex = '\\begin{axis}[\n' + indent(',\n'.join(options)) + ']\n'
		for child in self.children:
			tex += indent(child.render())
		tex += '\\end{axis}\n'

		return tex
