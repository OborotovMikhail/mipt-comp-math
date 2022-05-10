import matplotlib.pyplot as plt
import numpy as np

# Grid step
h = 1/20

# Area boundaries
xMin = -1
xMax = 1
yMin = -1
yMax = 1

# Number of point
xNum = int((xMax - xMin)/h)
yNum = int((yMax - yMin)/h)

# Initializing matrix and u
Matrix = np.zeros((xNum, yNum))
u = np.zeros((xNum, yNum))

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
def a(i):
	x = i * h
	return (x * x + 1.) / 10.

# Calculate boundary value
def calcBoundary(x, y):
    if (x == 0):
        return 1.
    if (x == 1):
        return y
    if (x == -1):
        return y * y
    if (y == 0):
        return 1.
    if (y == 1):
        return x
    if (y == -1):
        return x * x

# Check if a point in boundary (and calculate if it is)
def ifBoundary(i, j):
    x = i * h
    y = j * h
    if (x == 0) | (x == 1) | (x == -1) | (y == 0) | (y == 1) | (y == -1):
        return calcBoundary(x, y)
    else:
        return 0

# Main part
for l in range(0, yNum-1):
    for m in range(0, xNum-1):
        if (Matrix[m][l] == 0):
            if (ifArea(m, l) == 0):
                Matrix[m][l] = 0.
                u[m][l] = 0.
            else:
                if (ifBoundary(m, l) != 0):
                    Matrix[m][l] = 0.
                    u[m][l] = ifBoundary(m, l)
                else:
                    Matrix[m][l] = (-2*a(m) - (a(m+1) - a(m)))/(h*h)
            if (l != 0) & (l != yNum - 1) & (m != 0) & (m != xNum - 1):
                if (ifArea(m+1, l) == 0):
                    Matrix[m+1][l] = 0.
                    u[m+1][l] = 0.
                else:
                    if (ifBoundary(m+1, l) != 0):
                        Matrix[m+1][l] = 0.
                        u[m+1][l] = ifBoundary(m+1, l)
                    else:
                        Matrix[m + 1][l] = (a(m) + (a(m + 1) - a(m))) / (h * h)

                if (ifArea(m - 1, l) == 0):
                    Matrix[m - 1][l] = 0.
                    u[m - 1][l] = 0.
                else:
                    if (ifBoundary(m - 1, l) != 0):
                        Matrix[m - 1][l] = 0.
                        u[m - 1][l] = ifBoundary(m-1, l)
                    else:
                        Matrix[m-1][l] = a(m)/(h*h)

                if (ifArea(m, l+1) == 0):
                    Matrix[m][l+1] = 0.
                    u[m][l+1] = 0.
                else:
                    if (ifBoundary(m, l+1) != 0):
                        Matrix[m][l+1] = 0.
                        u[m][l+1] = ifBoundary(m, l+1)
                    else:
                        Matrix[m][l+1] = a(m)/(h*h)

                if (ifArea(m, l - 1) == 0):
                    Matrix[m][l - 1] = 0.
                    u[m][l - 1] = 0.
                else:
                    if (ifBoundary(m, l - 1) != 0):
                        Matrix[m][l - 1] = 0.
                        u[m][l - 1] = ifBoundary(m, l - 1)
                    else:
                        Matrix[m][l-1] = a(m)/(h*h)

print(Matrix)

# Matrix visualization
plt.matshow(Matrix, cmap='plasma')
plt.colorbar()
plt.show()
