from HSRindicator import HSRindicator as HSR
from plotInvestment import plot
import numpy as np


if __name__ == "__main__":
    
    # Example for 2 dimensions
    # Point set: {(1,3), (2,2), (3,1)},  l = (0,0), u = (4,4)
    A = np.array([[1,3],[2,2],[3,1]])           # matrix with dimensions n x d (n points, d dimensions)
    l = np.zeros(2)                             # l must weakly dominate every point in A
    u = np.array([4,4])                         # u must be strongly dominated by every point in A
    hsri, x = HSR(A,l,u)                        # compute HSR indicator

    print("Optimal investment:")
    print("%s" % "\n".join(map(str, x[:,0])))
    print("HSR indicator value: %f" % hsri)

    plot(A,x,l,u, saveTo="example-plots/plot")  # plot investment
