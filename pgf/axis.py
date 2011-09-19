from utils import indent, escape
from figure import Figure
from numpy import min, max, inf

class Axis(object):
	"""
	Manages axis properties.

	@type at: tuple/None
	@ivar at: axis position

	@type width: float
	@ivar width: axis width in cm

	@type height: float
	@ivar height: axis height in cm

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

	@type axis_type: string
	@ivar axis_type: 'axis', 'semilogxaxis', 'semilogyaxis' or 'loglogaxis'

	@type axis_x_line: string/None
	@ivar axis_x_line: x-axis position, e.g. 'middle', 'top', 'bottom', 'none'

	@type axis_y_line: string/None
	@ivar axis_y_line: y-axis position, e.g. 'center', 'left', 'right', 'none'

	@type ybar: boolean
	@ivar ybar: enables bar plot (or histogram)

	@type xbar: boolean
	@ivar xbar: enables horizontal bar plot

	@type bar_width: float/None
	@type bar_width: determines the bar width for bar plots in cm

	@type stacked: boolean
	@ivar stacked: if enabled, bar plots are stacked

	@type interval: boolean
	@ivar interval: if enabled, neighboring values determine bar widths

	@type colormap: string/None
	@ivar colormap: colormap used by some plots, e.g. 'hot', 'cool', 'bluered'

	@type cycle_list: CycleList/list/None
	@ivar cycle_list: a list of styles used for plots

	@type cycle_list_name: String/None
	@ivar cycle_list_name: a specific PGFPlots cycle list

	@type pgf_options: list
	@ivar pgf_options: custom PGFPlots axis options

	@type children: list
	@ivar children: list of plots contained in this axis
	"""

	@staticmethod
	def gca():
		"""
		Returns the currently active axis.

		@rtype: Axis
		@return: the currently active axis
		"""

		if not Figure.gcf()._ca:
			Axis()
		return Figure.gcf()._ca


	def __init__(self, fig=None, *args, **kwargs):
		"""
		Initializes axis properties.
		"""

		# parent figure
		self.figure = fig

		# legend
		self.legend = None

		# axis position
		self.at = kwargs.get('at', [0., 0.])

		# width and height of axis
		self.width = kwargs.get('width', 8.)
		self.height = kwargs.get('height', 7.)

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

		# linear or logarithmic axis
		self.axis_type = kwargs.get('axis_type', 'axis')

		# axis positions
		self.axis_x_line = kwargs.get('axis_x_line', None)
		self.axis_y_line = kwargs.get('axis_y_line', None)

		# bar plots
		self.ybar = kwargs.get('ybar', False)
		self.xbar = kwargs.get('xbar', False)
		self.bar_width = kwargs.get('bar_width', None)
		self.stacked = kwargs.get('stacked', False)
		self.interval = kwargs.get('interval', False)

		# controls aspect ratio
		self.equal = kwargs.get('equal', None)

		# color and style specifications
		self.colormap = kwargs.get('colormap', None)
		self.cycle_list = kwargs.get('cycle_list', None)
		self.cycle_list_name = kwargs.get('cycle_list_name', None)

		# grid lines
		self.grid = kwargs.get('grid', None)

		# custom axis options
		self.pgf_options = kwargs.get('pgf_options', [])

		if not self.figure:
			self.figure = Figure.gcf()

		# add axis to figure (if figure is not controlled by axis grid)
		from axisgrid import AxisGrid
		if not (self.figure.axes and isinstance(self.figure.axes[0], AxisGrid)):
			self.figure.axes.append(self)

		# make this axis active
		self.figure._ca = self


	def render(self):
		"""
		Produces the LaTeX code for this axis.

		@rtype: string
		@return: LaTeX code for this axis
		"""

		options = [
			'scale only axis',
			'width={0}cm'.format(self.width),
			'height={0}cm'.format(self.height)]

		if self.at is not None:
			options.append('at={{({0}cm, {1}cm)}}'.format(self.at[0], self.at[1]))

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
				options.append('{0}={{{1}}}'.format(
					prop, escape(str(self.__dict__[prop]))))

		# different properties
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

		# ticks and tick labels
		if self.xtick:
			options.append('xtick={{{0}}}'.format(
				','.join(str(t) for t in self.xtick)))
			if self.xticklabels:
				options.append('xtick scale label code/.code={}')
		elif self.xtick is not None:
			options.append('xtick=\empty')
			options.append('xtick scale label code/.code={}')
		if self.ytick:
			options.append('ytick={{{0}}}'.format(
				','.join(str(t) for t in self.ytick)))
			if self.yticklabels:
				options.append('ytick scale label code/.code={}')
		elif self.ytick is not None:
			options.append('ytick=\empty')
			options.append('ytick scale label code/.code={}')
		if self.xticklabels is not None:
			options.append('xticklabels={{{0}}}'.format(
				','.join(escape(self.xticklabels))))
		if self.yticklabels is not None:
			options.append('yticklabels={{{0}}}'.format(
				','.join(escape(self.yticklabels))))

		# axis positions
		if self.axis_x_line:
			options.append('axis x line={0}'.format(self.axis_x_line))
		if self.axis_y_line:
			options.append('axis y line={0}'.format(self.axis_y_line))

		# bar plots
		if self.ybar and self.interval:
			options.append('ybar interval')
			if not self.grid:
				options.append('grid=none')
		elif self.ybar and self.stacked:
			options.append('ybar stacked')
		elif self.ybar:
			options.append('ybar')
		elif self.xbar and self.interval:
			options.append('xbar interval')
			if not self.grid:
				options.append('grid=none')
		elif self.xbar and self.stacked:
			options.append('xbar stacked')
		elif self.xbar:
			options.append('xbar')
		if self.xbar or self.ybar:
			options.append('area legend')
		if self.bar_width:
			options.append('bar width={0}cm'.format(self.bar_width))

		# colors and line styles
		if self.colormap:
			options.append('colormap/{0}'.format(self.colormap))
		if self.cycle_list:
			options.append(self.cycle_list.render())
		elif self.cycle_list_name:
			options.append('cycle list name={0}'.format(self.cycle_list_name))

		# custom options
		options.extend(self.pgf_options)

		tex = '\\begin{{{0}}}[\n'.format(self.axis_type)
		tex += indent(',\n'.join(options)) + ']\n'
		for child in self.children:
			tex += indent(child.render())
		tex += '\\end{{{0}}}\n'.format(self.axis_type)

		return tex


	def limits(self):
		"""
		@rtype: list
		@return: [xmin, xmax, ymin, ymax]
		"""

		_xmin, _xmax = inf, -inf
		_ymin, _ymax = inf, -inf

		# find minimum and maximum of data points
		for child in self.children:
			xmin, xmax, ymin, ymax = child.limits()
			_xmin = min([_xmin, xmin])
			_xmax = max([_xmax, xmax])
			_ymin = min([_ymin, ymin])
			_ymax = max([_ymax, ymax])

		return [_xmin, _xmax, _ymin, _ymax]
