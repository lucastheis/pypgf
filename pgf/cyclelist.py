from rgb import RGB

class CycleList(object):
	def __init__(self, styles=None):
		self.entries = []

		for style in styles:
			if isinstance(style, list):
				self.append(*style)
			else:
				self.append(style)


	def __getitem__(self, key):
		return self.entries[key]


	def __getslice__(self, start, end):
		return self.entries[start:end]


	def __delitem__(self, key):
		del self.entries[key]

	
	def __delslice__(self, start, end):
		del self.entries[start:end]


	def append(self, *args, **kwargs):
		"""
		B{Examples:}

			>>> cl.append('red')
			>>> cl.append(RGB(0.5, 0.2, 1.0))
			>>> cl.append(color='black', fill='red')
			>>> cl.append('blue', 'dotted')
		"""

		if not args and not kwargs:
			raise TypeError('append() takes at least 1 argument')

		self.entries.append((args, kwargs))


	def render(self):
		def parse(arg):
			# makes sure that RGB values are represented correctly
			if isinstance(arg, RGB):
				return 'color=' + str(arg)
			return str(arg)

		# string representations of entries
		entries = []

		# generate string representations
		for entry in self.entries:
			for key, value in entry[1]:
				entry[0].append('key=' + str(value))
			entries.append('\t{' + ', '.join(parse(arg) for arg in entry[0]) + '}')

		return 'cycle list={\n' + ',\n'.join(entries) + '}'


# predefined cycle lists
cycle_lists = {
	'fancy': CycleList([
			[RGB(10, 80, 230)],
			[RGB(255, 83, 204)],
			[RGB(170, 250, 120)],
			[RGB(0, 0, 0)],
			[RGB(255, 200, 0)],
		])
}
