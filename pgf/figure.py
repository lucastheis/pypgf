from os import system
from utils import min_free, indent
from settings import Settings
from numpy.random import randint

class Figure(object):
	# currently active figure
	_figures = {}
	_cf = None
	_session = randint(1E8)

	@staticmethod
	def gcf():
		"""
		Returns currently active figure.
		"""

		if not Figure._cf:
			Figure()
		return Figure._cf


	def __new__(cls, idx=None, *args, **kwargs):
		if idx in Figure._figures:
			# move focus
			Figure._cf = Figure._figures[idx]

			# figure with specified ID already exists
			return Figure._cf
		else:
			# create new figure
			fig = object.__new__(cls, idx, *args, **kwargs)
			fig._idx = min_free(Figure._figures.keys())

			# store figure reference and move focus
			Figure._figures[fig._idx] = fig
			Figure._cf = fig

			return fig


	def __init__(self, *args, **kwargs):
		"""
		Initializes figure properties.
		"""

		self.axes = []

		# width and height of the figure
		self.width = None
		self.height = None

		# space around axes
		self.margin = kwargs.get('margin', 2.)


	def render(self):
		"""
		Creates and returns LaTeX code for this figure.

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
