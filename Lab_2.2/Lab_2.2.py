import matplotlib.pyplot as plt
import numpy as np

# Grid step
h = 1/20

# Area boundaries
xMax = 1
xMin = -1
yMax = 1
yMin = -1

# Checking if point is a part of the area
def ifArea(i, j):
	x = h * i
	y = h * j
	if (x > 0.) & (y < 0.):
		return 0
	else:
		return 1

# f(x, y) function and its boundaries, set by default
# (right side function)
def f(x, y):
    if (x >= -0.75) & (x <= -0.25) & (y >= 0.25) & (y <= 0.75):
        return 1.
    else:
        return 0.

# a(x, y) function, set by default
def a(x, y):
	return (x * x + 1.) / 10.




