class Settings(object):
	tmp_dir = '/tmp/'
	pdf_compile = 'pdflatex -halt-on-error -interaction batchmode {0} > /dev/null'
	pdf_view = 'open {0}'
	image_folder = 'images'
	image_format = 'PNG'
	preamble = \
		'\\usepackage[utf8]{inputenc}\n' + \
		'\\usepackage{amsmath}\n' + \
		'\\usepackage{amssymb}\n' + \
		'\\usepackage{pgfplots}\n' + \
		'\\usepgflibrary{arrows}\n'
