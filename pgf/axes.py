from utils import indent, escape
from figure import Figure
from numpy import min, max, inf

class Axes(object):
	"""
	Manages axes properties.

	@type at: tuple/None
	@ivar at: position of axes within figure

	@type width: float
	@ivar width: axis width in cm

	@type height: float
	@ivar height: axis height in cm

	@type title: string
	@ivar title: title above axes

	@type xlabel: string
	@ivar xlabel: label next to x-axis

	@type ylabel: string
	@ivar ylabel: label next to y-axis

	@type xmin: float/None
	@ivar xmin: lower limit of x-axis

	@type xmax: float/None
	@ivar xmax: upper limit of x-axis

	@type ymin: float/None
	@ivar ymin: lower limit of y-axis

	@type ymax: float/None
	@ivar ymax: upper limit of y-axis

	@type enlargelimits: boolean/None
	@ivar enlargelimits: add a margin between plots and axes

	@type xtick: list/None
	@ivar xtick: location of ticks at x-axis

	@type ytick: list/None
	@ivar ytick: location of ticks at y-axis

	@type xticklabel_precision: integer/None
	@ivar xticklabel_precision: precision of x-axis tick labels

	@type yticklabel_precision: integer/None
	@ivar yticklabel_precision: precision of y-axis tick labels

	@type xtick_align: string/None
	@ivar xtick_align: position ticks 'inside' or 'outside' of axes

	@type ytick_align: string/None
	@ivar ytick_align: position ticks 'inside' or 'outside' of axes

	@type xticklabels: list/None
	@ivar xticklabels: labeling of ticks

	@type yticklabels: list/None
	@ivar yticklabels: labeling of ticks

	@type equal: boolean/None
	@ivar equal: forces units on all axes to have equal lengths

	@type grid: boolean/None
	@ivar grid: enables major grid

	@type axes_type: string
	@ivar axes_type: 'axis', 'semilogxaxis', 'semilogyaxis' or 'loglogaxis'

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
	@ivar children: list of plots belonging to this axes object
	"""

	@staticmethod
	def gca():
		"""
		Returns the currently active axes object.

		@rtype: Axes
		@return: the currently active set of axes
		"""

		if not Figure.gcf()._ca:
			Axes()
		return Figure.gcf()._ca


	def __init__(self, fig=None, *args, **kwargs):
		"""
		Initializes axes properties.
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

		# plots belonging to these axes
		self.children = []

		# title above axes
		self.title = kwargs.get('title', '')

		# axes labels
		self.xlabel = kwargs.get('xlabel', '')
		self.ylabel = kwargs.get('ylabel', '')

		# axes limits
		self.xmin = kwargs.get('xmin', None)
		self.xmax = kwargs.get('xmax', None)
		self.ymin = kwargs.get('ymin', None)
		self.ymax = kwargs.get('ymax', None)

		# if true, put a margin between plots and axes
		self.enlargelimits = kwargs.get('enlargelimits', None)

		# tick positions
		self.xtick = kwargs.get('xtick', None)
		self.ytick = kwargs.get('ytick', None)

		# tick label precisions
		self.xticklabel_precision = kwargs.get('xticklabel_precision', 4)
		self.yticklabel_precision = kwargs.get('yticklabel_precision', 4)

		# tick positions
		self.xtick_align = kwargs.get('xtick_align', None)
		self.ytick_align = kwargs.get('ytick_align', None)

		# tick labels
		self.xticklabels = kwargs.get('xticklabels', None)
		self.yticklabels = kwargs.get('yticklabels', None)

		# linear or logarithmic axes
		self.axes_type = kwargs.get('axes_type', 'axis')

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

		# custom axes properties
		self.pgf_options = kwargs.get('pgf_options', [])

		if not self.figure:
			self.figure = Figure.gcf()

		# add axes to figure (if figure is not controlled by AxesGrid)
		from axesgrid import AxesGrid
		if not (self.figure.axes and isinstance(self.figure.axes[0], AxesGrid)):
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

		# automatically handled properties
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

		if self.enlargelimits is not None:
			options.append('enlargelimits={0}'.format(
				'true' if self.enlargelimits else 'false'))

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
		if self.xtick_align is not None:
			options.append('xtick align={{{0}}}'.format(self.xtick_align))
		if self.ytick_align is not None:
			options.append('ytick align={{{0}}}'.format(self.ytick_align))
		if self.xticklabel_precision is not None and self.axes_type in ['axis', 'semilogyaxis']:
			options.append(
				r'xticklabel={{\pgfmathprintnumber[precision={0}]{{\tick}}}}'.format(
					self.xticklabel_precision))
		if self.yticklabel_precision is not None and self.axes_type in ['axis', 'semilogxaxis']:
			options.append(
				r'yticklabel={{\pgfmathprintnumber[precision={0}]{{\tick}}}}'.format(
					self.yticklabel_precision))

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

		tex = '\\begin{{{0}}}[\n'.format(self.axes_type)
		tex += indent(',\n'.join(options)) + ']\n'
		for child in self.children:
			tex += indent(child.render())
		tex += '\\end{{{0}}}\n'.format(self.axes_type)

		return tex


	def limits(self):
		"""
		Computes the minimum and maximum values over all data points contained in
		these axes.

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



	def __getitem__(self, key):
		return self.limits()[key]
