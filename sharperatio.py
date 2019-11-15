__author__ = "Andreia P. Guerreiro"
__copyright__ = "Copyright (C) Andreia P. Guerreiro, Carlos M. Fonseca"
__license__ = "GNU General Public License, version 3"
__version__ = "0.1"

import numpy as np
import math
from cvxopt import solvers, matrix

solvers.options['abstol'] = 1e-15
solvers.options['reltol'] = 1e-15
solvers.options['feastol'] = 1e-15
solvers.options['maxiters'] = 1000
solvers.options['show_progress'] = False


def sharpeRatio(p, Q, x, rf):
    """ Compute the Sharpe ratio.
    
    Returns the Sharpe ratio given the expected return vector, p,
    the covariance matrix, Q, the investment column vector, x, and
    the return of the riskless asset, rf.
    
    Parameters
    ----------
    p : ndarray
        Expected return vector (of size n).
    Q : ndarray
        Covariance (n,n)-matrix.
    x : ndarray
        Investment vector of size (n,1). The sum of which should be 1.
    rf : float
        Return of a riskless asset.
        
    Returns
    -------
    sr : float
        The HSR value.
    """
    return (x.T.dot(p) - rf)/math.sqrt(x.T.dot(Q).dot(x))


def _sharpeRatioQPMax(p,Q,rf):
    """ Sharpe ratio maximization problem - QP formulation """
    n = len(p)
    
    #inequality constraints (investment in assets is higher or equal to 0)
    C = np.diag(np.ones(n))
    d = np.zeros((n, 1), dtype=np.double)
    
    #equality constraints (just one)
    A = np.zeros((1, n), dtype=np.double)
    b = np.zeros((1, 1), dtype=np.double)
    A[0,:] = p - rf
    b[0,0] = 1
    
    #convert numpy matrix to cvxopt matrix
    G, c, A, b, C, d = matrix(Q, tc='d'), matrix(np.zeros(n), tc='d'), matrix(A, tc='d'), matrix(b, tc='d'), matrix(C, tc='d'), matrix(d, tc='d')
    
    sol = solvers.coneqp(G, c, -C, -d, None, A, b, kktsolver='ldl') #, initvals=self.initGuess)
    y = np.array(sol['x'])
    
    return y



def sharpeRatioMax(p, Q, rf):
    """ Compute the Sharpe ratio and investment of an optimal portfolio.
    
    Parameters
    ----------
    p : ndarray
        Expected return vector (of size n).
    Q : ndarray
        Covariance (n,n)-matrix.
    rf : float
        Return of a riskless asset.
        
    Returns
    -------
    sr : float
        The HSR value.
    x : ndarray
        Investment vector of size (n,1).
    """
    y = _sharpeRatioQPMax(p, Q, rf)
    x = y/y.sum()
    x = np.where(x > 1e-9, x, 0)
    sr = sharpeRatio(p, Q, x, rf)
    return sr, x

