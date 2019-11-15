# HSR

This software implements the HSR indicator.
    
## License

This software is Copyright © 2014-2019 Andreia P. Guerreiro, Carlos M. Fonseca.

This program is free software. You can redistribute it and/or modify it under the terms of the GNU General Public License, version 3, as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

Appropriate reference to this software should be made when describing research in which it played a substantive role, so that it may be replicated and verified by others. The HSR indicator, which this software implements, was first proposed in [1], and was formalized, named, and theoretically studied in [2,3].


<!-- # Building -->


## Usage

This software is implemented in python, and is compatible both with python 2.7 and python 3. The following modules are required: `numpy`, `cvxopt`, and `matplotlib`.


### From command line

**Synopsis**

    hsr-main.py [-h] [-l L] [-u U] [-p] [-v] [-q] [-f {0,1,2}] FILE


**Description**

Compute the HSR indicator for the data set in FILE.

**Command line options**

		  -h, 		--help   		show this help message and exit
		  -l L         				set the lower reference point (default: "0 ... 0")
		  -u U         				set the upper reference point (default: "1 ... 1")
		  -p, 		--plot   		plot the input points and the corresponding investment
	        					  (available only for 2-dimensional point sets)
		  -v           				verbose mode
		  -q, 		--quiet  		quiet mode. Do not show warnings.
		  -f {0,1,2},	--format {0,1,2} 	output format.
							  (0: print the optimal investment in each point followed by
							      the HSR indicator value)
							  (1: print the optimal investment in each point)
							  (2: print the HSR indicator value).


**Run**

The program reads sets of points in the file specified in the command line:

    python hsr-main.py myfile

In the input file, each point is given in a separate line, and each coordinate within a line is separated by whitespace.

The lower reference point can be set by giving option -l.

    python hsr-main.py -l "-4 -4 -2" myfile


If no lower reference point is given, the default is the origin (0,...,0).

Similarly, the upper reference point can be set by giving option -u.

    python hsr-main.py -u "10 20 20" myfile

If no upper reference point is given, the default is (1,...,1).

**Note:** The default reference points assume a normalized data set. Ideally, the reference points should be set in such a way that the lower reference point weakly dominates every point in the data set, and every point in the data set strongly dominates the upper reference point. Be aware that, if this is not the case, the points that do not dominate the upper reference point will be assigned zero investment, and any point that does not weakly dominate the lower reference point is equivalent to replacing it by the coordinate-wise maximum between that point and the lower reference point. Moreover, if there is no point in the input set that strongly dominates the upper reference point, then the corresponding Sharpe-ratio indicator value will be zero.



#### Example 1


**Input File**

Example of valid content of input files:

	3.41e-01 9.72e-01 2.47e-01
	9.30e-01 1.53e-01 4.72e-01
	4.56e-01 1.71e-01 8.68e-01
	8.70e-02 5.94e-01 9.50e-01
	5.31e-01 6.35e-01 1.95e-01
	3.12e-01 3.37e-01 7.01e-01
	3.05e-02 9.10e-01 7.71e-01
	8.89e-01 8.29e-01 2.07e-02
	6.92e-01 3.62e-01 2.93e-01
	2.33e-01 4.55e-01 6.60e-01


**Execution**

The file `convex.3d.10.dat` in the `datasets` folder provided with this package contains the 3-dimensional example with the above set of 10 points. All points have coordinate values between 0 and 1, and thus, the default lower and upper reference points may be used by running;

	python hsr-main.py datasets/convex.3d.10.dat
	
The following output produced is the optimal investment in the input points given the reference points `(0,0)`and `(1,1)`, followed by the corresponding HSR value:

	0.0810630292149
	0.0851252037552
	0.0762546411666
	0.00696918672958
	0.213741611428
	0.126567309907
	0.0338216055371
	0.00758150784974
	0.194742924803
	0.174132979609
	0.540402

	
where the *i*-th line corresponds to the optimal investment in the *i*-th input point. The last line corresponds to the HSR indicator value (`0.540402`) of the input set.

 Note that option `-f`allows the user to decide whether only the investment or the HSR indicator value should be printed.


#### Example 2


**Input File**

The file `datasets/my2Dexample.inp`contains the following 2-dimensional point set, that includes dominated and duplicated points:

	40 48
	40 48
	3 81
	53 94
	76 81 
	6 48
	3 81
	74 53
	14 1
	59 -9
	3 81
	44 34
	59 -9
	83 -2

	
**Execution**

By running:

	python hsr-main.py datasets/my2Dexample.inp -l "-10 -10" -u "100 100" --plot
	
The following output is produced, which gives the optimal investment in each of the input points given the reference points `(-10,-10)`and `(100,100)`, followed by the corresponding HSR-indicator value:

	0.0
	0.0
	0.0401414529843	
	0.0
	0.0
	0.122685916737
	0.0
	0.0
	0.701524206263
	0.135648424015
	0.0
	0.0
	0.0
	0.0
	1.583823

	
The corresponding HSR-indicator value of the input set is `1.583823`. The following plot is also shown:

<img src=example-plots/pts-ex2.png width="300">


More examples of input files are provided in the `datasets` folder.



## From python

### Example

The following example (see `example.py`) calculates the HSR indicator for the 2-dimensional point set `A = {(1,3), (2,2), (3,1)}` given the lower reference point `l=(0,0)` and the upper reference point `u=(4,4)`. 

    from HSRindicator import HSRindicator as HSR
    from plotInvestment import plot
    import numpy as np
    
    # Example for 2 dimensions
    # Point set: {(1,3), (2,2), (3,1)},  l = (0,0), u = (4,4)
    A = np.array([[1,3],[2,2],[3,1]])   		# matrix with dimensions n x d (n points, d dimensions)
    l = np.zeros(2)                     		# l must weakly dominate every point in A
    u = np.array([4,4])                  		# u must be strongly dominated by every point in A
    hsri, x = HSR(A,l,u)                		# compute HSR indicator
    
    print("Optimal investment:")
    print("%s" % "\n".join(map(str, x[:,0])))
    print("HSR indicator value: %f" % hsri)
        
    plot(A,x,l,u, saveTo="example-plots/ptsA")  	# plot investment
    
The last line will show a figure with the points in `A` and their corresponding optimal investment, `x`, represented by a circle where the area of the circle centered at a point is proportional to the investment in such point. In addition, the figure is saved in `.png`and `.pdf`format in `example-plots/ptsA.png`and `example-plots/ptsA.pdf`, respectively. The figure generated in the above example is the following:

<img src=example-plots/ptsA.png width="300">
    
The output produced is the following:

	Optimal investment:
	0.333333333333
	0.333333333333
	0.333333333333
	HSR indicator value: 0.674200


# References


<!-- PPSN 2014 -->

[1] I. Yevseyeva, A.P. Guerreiro, M.T.M. Emmerich, C.M. Fonseca. *A Portfolio Optimization Approach to Selection in Multiobjective Evolutionary Algorithms*. Parallel Problem Solving from Nature – PPSN XIII, vol. 8672 of LNCS, pp. 672–681, 2014. [[pdf][PPSN14]]

[PPSN14]: https://eden.dei.uc.pt/~cmfonsec/paper-HSR-ppsn2016-authorVersion.pdf


<!-- PPSN 2016 -->
[2] A.P. Guerreiro, C.M. Fonseca. *Hypervolume Sharpe Ratio Indicator: Formalization and First Theoretical Results*. Parallel Problem Solving from Nature – PPSN XIV, vol. 9921 of LNCS, pp. 814–823, 2016.  [[pdf][PPSN16]]

[PPSN16]: https://eden.dei.uc.pt/~cmfonsec/posea-authorVersion.pdf

<!-- EJOR -->

[3] A. P. Guerreiro and C. M. Fonseca. *An Analysis of the Hypervolume Sharpe-Ratio Indicator*. European Journal of Operational Research – EJOR, 2019 (to appear).

