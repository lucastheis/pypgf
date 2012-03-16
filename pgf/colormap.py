from numpy import asarray

class Colormap(object):
	"""
	Represents a color map. Each color map is basically a list of 256 RGB values.
	"""

	def __init__(self, colors):
		"""
		Computes color map. If less than 256 RGB values are given, interpolates
		linearly between the colors.

		@type  colors: list
		@param colors: a list of tuples or lists encoding RGB colors
		"""

		if len(colors) < 256:
			self.colors = []

			for i in range(256):
				j = (len(colors) - 1.) / 255. * i
				k = int(j)
				w = j - k

				if k < len(colors) - 1:
					self.colors.append(
						asarray(colors[k]) * (1. - w) + asarray(colors[k + 1]) * w)
					self.colors[-1] = asarray(self.colors[-1] + 0.5, 'uint8').tolist()
				else:
					self.colors.append(colors[k])
					
		else:
			self.colors = colors



	def __getitem__(self, key):
		return self.colors[key]



colormaps = {
	'gray': Colormap([
		[0, 0, 0],
		[255, 255, 255],
		]),
	'jet': Colormap([
		[0, 0, 144],
		[0, 0, 255],
		[0, 255, 255],
		[255, 255, 0],
		[255, 0, 0],
		[128, 0, 0],
		]),
	'hsv': Colormap([
		[255, 0, 0],
		[255, 255, 0],
		[0, 255, 0],
		[0, 255, 255],
		[0, 0, 255],
		[255, 0, 255],
		[255, 0, 0],
		]),
	'winter': Colormap([
		[0, 0, 255],
		[0, 255, 128],
		]),
	'cool': Colormap([
		[0, 255, 255],
		[255, 0, 255],
		]),
	'hot': Colormap([
		[0, 0, 0],
		[255, 0, 0],
		[255, 255, 0],
		[255, 255, 255],
		]),
	'cold': Colormap([
		[0, 0, 0],
		[0, 0, 255],
		[0, 255, 255],
		[255, 255, 255],
		]),
}
