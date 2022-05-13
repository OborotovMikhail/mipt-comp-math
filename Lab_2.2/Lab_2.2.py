import matplotlib.pyplot as plt
import numpy as np

############### Parameters ###############

# Grid step (set as a parameter)
h = 1/20

# Area boundaries (set as a parameter)
# Area is corner-shaped
xMin = -1
xMax = 1
yMin = -1
yMax = 1

# Number of points
xPoints = int((xMax - xMin) / h + 1)
yPoints = int((yMax - yMin) / h + 1)

# Get i (step number, knowing index of the point
def geti(index):
    global xPoints
    return index % xPoints

def getj(index):
    global xPoints
    return index // xPoints

# Get x value in point with index i
def x(i):
    global xMin, h
    return xMin + i * h

# Get y value in point with index j
def y(j):
    global yMin, h
    return yMin + j * h

# Function f(x,y) (set as a parameter)
def f(x, y):
    return 1

# Function a(x,y) (set as a parameter)
def a(x, y):
    return (x ** 2 + 1) / 10

# Function a(x,y) derivative with respect to x (set as a parameter)
def a_x(x, y):
    return x / 5

# Function a(x,y) derivative with respect to y (set as a parameter)
def a_y(x, y):
    return 0

print(geti(43))
print(getj(43))

############### Calculating the matrix ###############

Matrix = [] # Initializing matrix a 1D array for now
validPoints = [] # Initializing valid points (array of their indexes)

# Calculating valid point indexes according to our area
# Border points are not included, only those inside the area
# (Counting from the top left corner, going right)
for i in range(xPoints):
    for j in range(yPoints):
        # Including indexes inside the area (without borders)
        if (i != 0 and j != 0 and i != (xPoints - 1) and j != (yPoints - 1)):
            if (i < ((xPoints - 1) / 2) or j < ((yPoints - 1) / 2)):
                index = xPoints * j + i # Point index in the 1D array
                validPoints.append(int(index))

print("\nNumber of valid points: ", len(validPoints), "\n") # DEBUG

debugMatrCalcCurrent = 0 # DEBUG
debugMatrCalcTotal = len(validPoints) # DEBUG (total matrix calc iterations)

# Calculating values for the matrix elements
for validIndex in validPoints:
    # For each valid index running through all area points (also all valid indexes)
    for index in validPoints:
        if (index == validIndex):
            # Matrix element for point (i,j)
            element = -4 * 0
        elif ((index - validIndex) == -1):
            # Matrix element for point (i-1,j)
            element = 0
        elif ((index - validIndex) == 1):
            # Matrix element for point (i+1,j)
            element = 0
        elif ((index - validIndex) == -xPoints):
            # Matrix element for point (i,j-1)
            element = 0
        elif ((index - validIndex) == xPoints):
            # Matrix element for point (i,j+1)
            element = 0
        else:
            # Matrix element for all other points
            element = 0
        # Adding calculated element to the matrix
        Matrix.append(element)

    debugMatrCalcCurrent += 1 # DEBUG
    print("Matrix calculation iteration: ", debugMatrCalcCurrent, " of ", debugMatrCalcTotal) # DEBUG


print("\nNumber of matrix elements: ", len(Matrix), "\n") # DEBUG

