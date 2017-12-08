import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.widgets import Slider, Button, RadioButtons


# Assign initial parameters
R0=1
B0=0
eta0=0
eps0=0

# r is the same regardless of B
r=R0*np.multiply(eta0,eps0)

# Special Bluntness cases
if B0 == 0:
	x=R0/2*(1+np.square(eps0)-np.square(eta0))
elif B0 == 1:
	x=R0*(1-np.sqrt(1-np.multiply(np.square(eps0),eta0)))
else:
	 x=R0/B0*(np.sqrt(1-B0*np.square(eps0)*(1-B0+B0*np.square(eta0))))

def widget_init():
	global sR, sB, seta, seps, trace_button, reset_button
	axcolor = 'lightgoldenrodyellow'
	axeta = plt.axes([0.25, 0.16, 0.65, 0.03], facecolor=axcolor)
	axeps = plt.axes([0.25, 0.11, 0.65, 0.03], facecolor=axcolor)
	axR = plt.axes([0.25, 0.06, 0.65, 0.03])
	axB = plt.axes([0.25, 0.01, 0.65, 0.03])

	sR = Slider(axR, 'R', 0.01, 1, valinit=R0)
	sB = Slider(axB, 'B', 0, 1, valinit=B0)
	seta = Slider(axeta, 'eta', -1, 1, valinit=eta0)
	seps = Slider(axeps, 'eps', -1, 1, valinit=eps0)

	traceax = plt.axes([0.08, 0.11, 0.1, 0.04])
	trace_button = Button(traceax, 'Trace?', color=axcolor, hovercolor='0.975')
	trace = False

	resetax = plt.axes([0.08, 0.01, 0.1, 0.04])
	reset_button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

def plot_init():
	global fig, ax
	fig, ax = plt.subplots()
	plt.subplots_adjust(left=0.25, bottom=0.30)
	global l
	l, = plt.plot(x,r,'go')

	global circ
	circ=mpatches.Circle((R0, 0), R0, color='b', fill=False)
	ax.add_patch(circ)

	ax.grid(linestyle='-')
	plt.xlabel('x')
	plt.ylabel('r')
	ax.set_xlim(-1,1)
	ax.set_ylim(-1,1)
	ax.set_aspect('equal',adjustable='box')

	widget_init()

plot_init()

def update(val):
	global x
	global r
	x_old = x
	r_old = r
	eta = seta.val
	eps = seps.val
	R 	= sR.val
	B 	= sB.val

	r = R*eta*eps
	l.set_ydata(r)
	if B == 0:
		x=R/2*(1+np.square(eps)-np.square(eta))
	elif B == 1:
		x=R*(1-np.sqrt(1-np.multiply(np.square(eps),eta)))
	else:
		x=R/B*(np.sqrt(1-B*np.square(eps)*(1-B+B*np.square(eta))))
	l.set_xdata(x)

	global trace
	if trace == True:
		plt.sca(ax)
		ax.plot([x_old,x],[r_old,r],'-')

	global circ
	circ.remove()
	circ=mpatches.Circle((R, 0), R, color='b', fill=False)
	ax.add_patch(circ)

	fig.canvas.draw_idle()

seta.on_changed(update)
seps.on_changed(update)
sR.on_changed(update)
sB.on_changed(update)

def trace(event):
	global trace
	trace = not trace

trace_button.on_clicked(trace)

def reset(event):
	sR.reset()
	sB.reset()
	seta.reset()
	seps.reset()
	plt.close(fig)
	plot_init()
	plt.show()

reset_button.on_clicked(reset)

plt.show()