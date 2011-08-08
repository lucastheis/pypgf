from numpy import asarray, arange, min, max
from axis import Axis
from string import replace
from re import match
from rgb import RGB
from utils import indent

class Plot(object):
	"""
	Represents line plots.

	@type axis: L{Axis}
	@ivar axis: reference to assigned axis

	@type xvalues: array_like
	@ivar xvalues: x-coordinates of data points

	@type yvalues: array_like
	@ivar yvalues: y-coordinates of data points

	@type line_style: string/None
	@ivar line_style: solid, dashed, dotted or other line styles

	@type line_width: float/None
	@ivar line_width: line width in points

	@type opacity: float/None
	@ivar opacity: opacity between 0.0 and 1.0

	@type color: string/L{RGB}/None
	@ivar color: line and marker color

	@type marker: string/None
	@ivar marker: marker style in PGFPlots notation

	@type marker_size: float/None
	@ivar marker_size: marker size

	@type marker_edge_color: string/L{RGB}/None
	@ivar marker_edge_color: marker border color

	@type marker_face_color: string/L{RGB}/None
	@ivar marker_face_color: marker color

	@type marker_opacity: float/None
	@ivar marker_opacity: marker opacity between 0.0 and 1.0

	@type pgf_options: list
	@ivar pgf_options: custom PGFPlots plot options
	"""

	def __init__(self, *args, **kwargs):
		"""
		Initializes plot properties.
		"""

		# add plot to axis
		self.axis = kwargs.get('axis', Axis.gca())
		self.axis.children.append(self)

		# data points
		if len(args) < 1:
			self.xvalues = asarray([])
			self.yvalues = asarray([])
		elif len(args) < 2:
			self.yvalues = asarray(args[0]).flatten()
			self.xvalues = arange(1, len(self.yvalues) + 1)
		else:
			self.xvalues = asarray(args[0]).flatten()
			self.yvalues = asarray(args[1]).flatten()

		# line style
		self.line_style = kwargs.get('line_style', 'solid')
		self.line_width = kwargs.get('line_width', None)
		self.opacity = kwargs.get('opacity', None)
		self.color = kwargs.get('color', None)

		# marker style
		self.marker = kwargs.get('marker', 'no marker')
		self.marker_size = kwargs.get('marker_size', None)
		self.marker_edge_color = kwargs.get('marker_edge_color', None)
		self.marker_face_color = kwargs.get('marker_face_color', None)
		self.marker_opacity = kwargs.get('marker_opacity', None)

		# custom plot options
		self.pgf_options = kwargs.get('pgf_options', [])


	def render(self):
		"""
		Produces LaTeX code for this plot.

		@rtype: string
		@return: LaTeX code for this plot
		"""

		options = list(self.pgf_options)
		marker_options = ['solid']

		if self.line_style:
			options.append(self.line_style)
		else:
			options.append('only marks')
		if self.line_width:
			options.append('line width={0}pt'.format(self.line_width))
		if isinstance(self.color, RGB):
			options.append('color={0}'.format(self.color))
		elif isinstance(self.color, str):
			options.append(self.color)
		if self.opacity:
			options.append('opacity={0}'.format(self.opacity))
		if self.marker:
			options.append('mark={0}'.format(replace(self.marker, '.', '*')))
		else:
			options.append('no marks')
		if self.marker_edge_color:
			marker_options.append(str(self.marker_edge_color))
		if self.marker_face_color:
			marker_options.append('fill={0}'.format(self.marker_face_color))
		if self.marker_size is not None:
			marker_options.append('scale={0}'.format(self.marker_size))
		if self.marker_opacity is not None:
			marker_options.append('fill opacity={0}'.format(self.marker_opacity))
		elif self.opacity is not None:
			marker_options.append('fill opacity={0}'.format(self.opacity))
		if marker_options:
			options.append('mark options={{{0}}}'.format(', '.join(marker_options)))

		options_string = ', '.join(options)
		if len(options_string) > 60:
			options_string = '\n' + indent(',\n'.join(options))

		tex = '\\addplot+[{0}] coordinates {{\n'.format(options_string)
		for x, y in zip(self.xvalues, self.yvalues):
			tex += '\t({0}, {1})\n'.format(x, y)
		tex += '};\n'

		return tex


	def limits(self):
		"""
		Returns data point limits as [xmin, xmax, ymin, ymax].

		@rtype: list
		@return: data point limits
		"""
		return [
			min(self.xvalues),
			max(self.xvalues),
			min(self.yvalues),
			max(self.yvalues)]
