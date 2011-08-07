from numpy import asarray, arange, min, max
from axis import Axis
from string import replace
from re import match

class Plot(object):
	def __init__(self, *args, **kwargs):
		# add plot to axis
		self.axis = kwargs.get('axis', Axis.gca())
		self.axis.plots.append(self)

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
		self.opacity = kwargs.get('opacity', None)
		self.color = kwargs.get('color', 'blue')

		# marker style
		self.marker = kwargs.get('marker', 'no marker')
		self.marker_size = kwargs.get('marker_size', None)
		self.marker_edge_color = kwargs.get('marker_edge_color', None)
		self.marker_face_color = kwargs.get('marker_face_color', None)
		self.marker_opacity = kwargs.get('marker_opacity', None)


	def render(self):
		options = []
		marker_options = ['solid']

		if self.line_style:
			options.append(self.line_style)
		else:
			options.append('only marks')
		if self.color:
			options.append(str(self.color))
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

		tex = '\\addplot+[{0}] coordinates {{\n'.format(', '.join(options))
		for x, y in zip(self.xvalues, self.yvalues):
			tex += '\t({0}, {1})\n'.format(x, y)
		tex += '};\n'

		return tex


	def limits(self):
		return [
			min(self.xvalues),
			max(self.xvalues),
			min(self.yvalues),
			max(self.yvalues)]
