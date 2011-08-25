from numpy import min, max
from string import rstrip

def indent(text, times=1, ind='\t'):
	"""
	Indent text with multiple lines.

	@type  text: string
	@param text: some text

	@type  times: integer
	@param times: number of indentations

	@type  ind: string
	@param ind: string inserted at the beginning of each line
	"""

	if times > 1:
		text = indent(text, times - 1)
	return '\n'.join([rstrip(ind + line) for line in text.split('\n')])


def min_free(indices):
	if not indices:
		return 0
	return min(list(set(range(max(indices) + 2)).difference(indices)))


def braces(string):
	"""
	If string contains commas, put curly braces around it.

	@type  string: string/list
	@param string: e.g. a legend entry or axis label

	@rtype: string/list
	@return: processed string(s)
	"""

	if isinstance(string, list):
		return [braces(str(s)) for s in string]

	if ',' in string:
		return '{' + string + '}'

	return string
