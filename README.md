pypgf
=====

A Python interface for creating LaTeX plots with Christian Feuersänger's
[PGFPlots][1] and Till Tantau's [PGF/TikZ][2] package. The interface is still at
a very rudimentary stage, might change heavily in the future and lacks
documentation. Right now, only Mac and Linux are supported.

[1]: http://sourceforge.net/projects/pgfplots/
[2]: http://sourceforge.net/projects/pgf/

Requirements
------------

* Python >= 2.6.0
* NumPy >= 1.3.0
* PIL
* pdflatex
* PGF/TikZ
* PGFPlots >= 1.4.0

Example
-------

	from pgf import *
	from numpy import *

	plot(sin(linspace(-10, 10, 200)), 'r--')
	plot(cos(linspace(-10, 10, 200)), 'b--')
	legend('$\sin(x)$', '$\cos(x)$')
	draw()

The `draw()` command at the end compiles the figure and tries to open it in a
PDF viewer.


Troubleshooting
---------------

If `draw()` fails to show anything, have a look at `settings.py` and check whether
the settings are appropriate for your environment.

Another possible cause might be an outdated PGFPlots package. Try to figure out the
version installed on your computer using

	cat $(kpsewhich pgfplots.sty) | grep pgfplotsversion

If the version number is lower than 1.4.0, [download][1] the latest version.
To install the package, locate the old files with `kpsewhich pgfplots.sty`
and replace them with the downloaded files. Afterwards, run `texhash`. See the
PGFPlots manual for further instructions.
