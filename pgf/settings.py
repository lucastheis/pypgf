class Settings(object):
	tmp_dir = '/tmp/'
	command = 'pdflatex -halt-on-error -interaction batchmode {0} > /dev/null'
	preamble = \
		'\\usepackage[utf8]{inputenc}\n' + \
		'\\usepackage{amsmath}\n' + \
		'\\usepackage{amssymb}\n' + \
		'\\usepackage{pgfplots}\n'
