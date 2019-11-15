__author__ = "Andreia P. Guerreiro"
__copyright__ = "Copyright (C) Andreia P. Guerreiro"
__license__ = "GNU General Public License, version 3"
__version__ = "1.0"

import sharperatio as sr
import numpy as np


#np.random.seed(1)

# Assumes that l <= A << u
# Assumes A, l, u are numpy arrays
def _expectedReturn(A, l, u):
    """
    Returns the expected return (computed as defined by the HSR indicator), as a
    column vector.
    """
    A = np.array(A, dtype=np.double)        #because of division operator in python 2.7
    return ((u - A).prod(axis=-1))/((u - l).prod())


def _covariance(A, l, u, p=None):
    """  Returns the covariance matrix (computed as defined by the HSR indicator). """
    p = _expectedReturn(A,l,u) if p is None else p
    Pmax = np.maximum(A[:,np.newaxis,:], A[np.newaxis,...])
    P = _expectedReturn(Pmax,l,u)
    
    Q = P - p[:,np.newaxis] * p[np.newaxis,:]
    return Q
    
def _argunique(pts):
    """ Find the unique points of a matrix. Returns their indexes. """
    ix = np.lexsort(pts.T)
    diff = (pts[ix][1:] != pts[ix][:-1]).any(axis=1)
    un = np.ones(len(pts), dtype=bool)
    un[ix[1:]] = diff
    return un



def HSRindicator(A,l,u, managedup=False):
    """ 
    Compute the HSR indicator of the point set A given reference points l and u.
    
    Returns the HSR value of A given l and u, and returns the optimal investment.
    By default, points in A are assumed to be unique.
    
    Tip: Either ensure that A does not contain duplicated points
        (for example, remove them previously and then split the
        investment between the copies as you wish), or set the flag
        'managedup' to True.
        
    Parameters
    ----------
    A : ndarray
        Input matrix (n,d) with n points and d dimensions.
    l : array_like
        Lower reference point.
    u : array_like
        Upper reference point.
    managedup : bool, optional
        If A contains duplicated points and 'managedup' is set to True, only the
        first copy may be assigned positive investment, all other copies are
        assigned zero investment. Otherwise, no special treatment is given to
        duplicate points.
        
    Returns
    -------
    hsri : float
        The HSR value.
       x : ndarray
        The optimal investment as a column vector array (n,1).
    """
    n = len(A)
    x = np.zeros((n,1), dtype=float)

    #if u is not strongly dominated by l or A is the empty set
    if (u <= l).any():
        raise ValueError("The lower reference point does not strongly"\
            "dominate the upper reference point!")
    
    if len(A) == 0:
        return 0, x
    
    valid = (A < u).all(axis=1)
    validix = np.where(valid)[0]
    
    #if A is the empty set
    if valid.sum() == 0:
        return 0, x
    A = A[valid]            #A only contains points that strongly dominate u
    A = np.maximum(A, l)
    m = len(A) #new size (m <= n)
    
    #manage duplicate points
    ix = _argunique(A) if managedup else np.ones(m).astype(bool)
    p = _expectedReturn(A[ix],l,u)
    Q = _covariance(A[ix],l,u,p)
    
    hsri, x[validix[ix]] = sr.sharpeRatioMax(p,Q,0)
    
    return hsri, x
    
