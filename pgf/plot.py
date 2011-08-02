from numpy import asarray, arange
from axis import Axis

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

		# line style
		self.line_style = kwargs.get('line_style', None)

		# marker style
		self.marker = kwargs.get('marker', None)
		self.marker_size = kwargs.get('marker_size', 1)
		self.marker_edge_color = kwargs.get('marker_edge_color', None)
		self.marker_face_color = kwargs.get('marker_face_color', None)

		# opacity
		self.opacity = kwargs.get('opacity', None)
		self.fill_opacity = kwargs.get('fill_opacity', None)


	def render(self):
		# default
		color = 'blue'
		line_style = 'solid'
		marker = 'no marks'
		marker_options = ['scale={0}'.format(self.marker_size)]

		# line style
		if self.line_style:
			line_style = self.line_style

		# marker style
		if self.marker:
			marker = 'mark={0}'.format(marker)

		# marker options
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
		if '---' in self.format_string:
			line_style = 'densely dashed'
		elif '--' in self.format_string:
			line_style = 'dashed'
		elif '-' in self.format_string:
			line_style = 'solid'
		elif ':' in self.format_string:
			line_style = 'densely dotted'

		if (marker != 'no marks') \
			and '-' not in self.format_string \
			and ':' not in self.format_string \
			and not self.line_style:
			line_style = 'only marks'

		if marker_options:
			marker += ', mark options={' + ', '.join(marker_options) + '}'

		options = [color, line_style, marker]
		if self.opacity is not None:
			options.append('opacity={0}'.format(self.opacity))

		# produce LaTeX code
		tex = '\\addplot+[{0}] coordinates {{\n'.format(
			', '.join(options))
		for x, y in zip(self.xvalues, self.yvalues):
			tex += '\t({0}, {1})\n'.format(x, y)
		tex += '};\n'

		return tex
