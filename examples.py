from numpy import *
from numpy.random import *
from pgf import *

plot(randn(1000), randn(1000), 'r.', opacity=.5)
plot(randn(1000) / 2, randn(1000) / 2, 'b.', opacity=.5)

axis('equal')
axis([-5, 5, -5, 5])
grid('on')
legend(r'$\sigma = 1$', r'$\sigma = \frac{1}{2}$')
xlabel('$x$')
ylabel('$y$')
title('Gaussian distributions')

draw()



figure()

x = linspace(0, 10)

subplot(0, 0)
plot(x, cos(x), 'k', line_style='dotted', line_width=2)
title('Cosine')

subplot(0, 1)
plot(x, sin(x), 'k--.')
title('Sine')

draw()



figure()

hist(randn(100000), 50, density=True, color=RGB(0.2, 0.2, 0.2), fill='gray')
axis([-5, 5, 0, 0.5])

draw()



figure()

cyclelist('icy')

barh(rand(5))
barh(rand(5))
barh(rand(5))
barh(rand(5))

legend('1700', '1800', '1900', '2000', location='outer north east')
axis([0, 1, 0.5, 5.5])
ytick([1, 2, 3, 4, 5], ['(a)', '(b)', '(c)', '(d)', '(e)'])
xtick([0., 0.2, 0.4, 0.6, 0.8, 1.], ['0%', '20%', '40%', '60%', '80%', '100%'])
grid('on')

gca().height, gca().width = 10, 8

draw()

# save LaTeX code
save('examples.tex')
