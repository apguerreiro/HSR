__author__ = "Andreia P. Guerreiro"
__copyright__ = "Copyright (C) Andreia P. Guerreiro"
__license__ = "GNU General Public License, version 3"
__version__ = "1.0"


from HSRindicator import HSRindicator as HSR
from plotInvestment import plot
import numpy as np
import argparse
import warnings
import sys

def parseFile(fname):
    try:
        data = np.loadtxt(fname, dtype=float, ndmin=2)
    except:
        print("Could not read a point set from %s." % fname)
        sys.exit()
    if len(data) == 0:
        print("Empty file.")
        sys.exit()
        
    d = len(data[0])
    return data


def parseReferencePoint(r, d):    
    if r is not None:
        try:
            r = list(map(float, r.split()))
        except:
            print("Invalid reference point: \"%s\"." % r)
            sys.exit()
        #print "r:", r
        if len(r) != d:
            print("The number of dimensions of the reference point \"%s\" "
            "is incorrect (%d != %d)." % (" ".join(map(str, r)), len(r), d))
            sys.exit()

    return np.array(r)

def checkReferencePoints(data, l, u,):
    if not (l[np.newaxis, :] <= data).all():
        warnings.warn("The lower reference point does not weakly dominate all points in the input set.")
        #sys.exit()
        
    if not (data < u[np.newaxis, :]).all():
         warnings.warn("Not all points in the input set strongly dominate the upper reference point.")
        #sys.exit()
        

def parseArgs(fname, l, u, show, verbose=False):
    
    data = parseFile(fname)
    amin = np.amin(data, axis=0)
    amax = np.amax(data, axis=0)
    
    n = len(data)
    d = len(data[0])
    
    if d < 2:
        print("The point set in FILE has less than 2 dimensions.")
        sys.exit()
    
    if verbose:
        print("# Point set size: %d" % n)
        print("# Number of dimensions: %d" % d)
        print("# Coordinate-wise minimum: %s" % " ".join(map(str, amin)))
        print("# Coordinate-wise maximum: %s" % " ".join(map(str, amax)))
    
    #eps = (amax-amin)/n
    #l = amin - eps if l is None else parseReferencePoint(l, d)
    #u = amax + eps  if u is None else parseReferencePoint(u, d)

    l = np.zeros(d, dtype=float) if l is None else parseReferencePoint(l, d)
    u = np.ones(d, dtype=float)  if u is None else parseReferencePoint(u, d)
        
        
    if verbose:
        print("# Lower reference point: %s" % " ".join(map(str, l)))
        print("# Upper reference point: %s" % " ".join(map(str, u)))
        
    if (u <= l).any():
        print("The lower reference point does not strongly dominate the upper reference point!")
        sys.exit()
        
    checkReferencePoints(data, l, u)
    
    if show and d > 2:
         warnings.warn("The point set has more than 2 dimensions. No plot will be showned.")
        
    return data, np.array(l), np.array(u)


def readArguments():
    parser = argparse.ArgumentParser(description="Calculate the Hypervolume Sharpe-ratio (HSR) \
                                     indicator of the point set in FILE. Prints the optimal \
                                     investment and the corresponding HSR value.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("FILE", type=str, help="read point set from FILE")
    parser.add_argument("-l", type=str, help="set the lower reference point (default: \"0 ... 0\")")
    parser.add_argument("-u", type=str, help="set the upper reference point (default: \"1 ... 1\")")
    parser.add_argument("-p", "--plot", default=False, action="store_true", help="plot the input "\
                        "points and the corresponding investment\n(available only for 2-dimensional point sets)")
    parser.add_argument("-v", default=False, action="store_true", help="verbose mode")
    parser.add_argument("-q", "--quiet", default=False, action="store_true", help="quiet mode. Do not show warnings.")
    parser.add_argument("-f", "--format", default=0, type=int, choices=[0,1,2], help="output format.\n" \
                        "(0: print the optimal investment in each point followed by\n    the HSR indicator value)\n" \
                        "(1: print the optimal investment in each point)\n"\
                        "(2: print the HSR indicator value).")
    args = parser.parse_args(sys.argv[1:])
    #print("args:", args)
    fname = args.FILE
    
    if args.quiet:
        warnings.filterwarnings('ignore')
    
    data, l, u = parseArgs(fname, args.l, args.u, args.plot, verbose=args.v)
    
    return data, l, u, args.plot, args.v, args.format
    

if __name__ == "__main__":
    
    A, l, u, show, verbose, oformat = readArguments()
    
    hsri, x = HSR(A,l,u, managedup=True)

    if oformat in [0,1]:
        if verbose:
            print("# Optimal investment:")
        print("%s" % "\n".join(map(str, x[:,0])))
    
    if oformat in [0,2]:
        if verbose:
            print("# HSR indicator value:")
        print("%f" % hsri)
    
    if show and len(A[0]) == 2:
        plot(A,x,l,u)
    
