__author__ = "Andreia P. Guerreiro"
__copyright__ = "Copyright (C) Andreia P. Guerreiro, Carlos M. Fonseca"
__license__ = "GNU General Public License, version 3"
__version__ = "1.0"

import matplotlib.pyplot as plt
import HSRindicator as hsr
import numpy as np
from math import sqrt
import sys


def _plot2D(pts, x, l, u, saveTo=None):
    n = len(pts)
    fig=plt.figure(1,figsize=(4.5,4.5))
    fig.gca().set_aspect('equal')

    plt.plot(pts[:,0],pts[:,1],'.')

    for i in range(n):
        plt.plot(pts[i,0],pts[i,1],'bo',markerfacecolor='None',markeredgewidth=1,markersize=sqrt(64*n*x[i]))


    plt.axis([l[0],u[0],l[1],u[1]])
    plt.xlabel('Objective 1')
    plt.ylabel('Objective 2')

    if saveTo is not None:
        plt.savefig(saveTo+".png")
        plt.savefig(saveTo+".pdf")

    plt.show()
    



def plot(pts, x, l, u, saveTo=None):
    """
    Plot the (2-dimensional) points and the investment assigned to each of them.
    
    Plot the points 'pts' inside the region delimited by the lower and the upper
    reference points, l and u, respectively. The area of the circle centered at a
    point is proportional to the investment in such point. The investment is given
    in the vector x. The figure is saved to the filename provided in 'saveTo' both
    in .png and .pdf.
    """
    if len(pts[0]) == 2:
        _plot2D(pts, x, l, u, saveTo=saveTo)
    else:
        raise NotImplemented

