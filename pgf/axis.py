from utils import indent
from figure import Figure

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
