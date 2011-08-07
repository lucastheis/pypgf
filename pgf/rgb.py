class RGB:
	"""
	Generates RGB colors in PGF format.

	@type red: integer
	@ivar red: value between 0 and 255

	@type green: integer
	@ivar green: value between 0 and 255

	@type blue: integer
	@ivar blue: value between 0 and 255
	"""

	def __init__(self, red, green, blue):
		if not isinstance(red, int) or \
			not isinstance(green, int) or \
			not isinstance(blue, int):
			raise TypeError('Colors should be specified as integer.')

		if not (0 <= red <= 255) or \
			not (0 <= green <= 255) or \
			not (0 <= blue <= 255):
			raise ValueError('Color values should be between 0 and 255.')

		self.red = red
		self.green = green
		self.blue = blue


	def __str__(self):
		return '{{rgb:red,{0};green,{1};blue,{2}}}'.format(
			self.red, self.green, self.blue)
