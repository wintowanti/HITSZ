import numpy as np
import pylab as pl

x = [2,2,8,5,7,6,1,4,7,1,3]
y = [10,5,4,8,5,4,2,9,3,3,9]

x1 = [3.5,7,1.333333]
y1 = [9,4,3.33333]

pl.axis([0,9,0,11]);
pl.plot(x,y,"o")
pl.plot(x1,y1,"or");
pl.show()
