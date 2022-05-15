import sys
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

############### Parameters ###############

# Grid step (set as a parameter)
h = 1/20

# Area boundaries (set as a parameter)
# Area is corner-shaped!
xMin = -1 # Must be < 0
xMax = 1  # Must be > 0
yMin = -1 # Must be < 0
yMax = 1  # Must be > 0

# Number of points
xPoints = int((xMax - xMin) / h + 1)
yPoints = int((yMax - yMin) / h + 1)

# Area in which right side (f(x,y) function) is defined
f_xMin = xMin - xMin / 4
f_xMax = xMin / 4
f_yMin = yMax / 4
f_yMax = yMax - yMax / 4

############### Functions set as a parameter ###############

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

############### Supporting functions ###############

# Get i (step number along x axis), knowing index of the point
def geti(index):
    global xPoints
    return index % xPoints

# Get j (step number along y axis), knowing index of the point
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
    return yMax - j * h

# Fuction used to reshape 1D corner-area data array
# to a 2D square-area data matrix
# (Used to plot data)
def reshapeToSquare(validPoints, data):
    # validPoints - is an array of indexes of points in the corner-area
    # data - is an array of values is these points

    global xPoints, yPoints

    # Initializing a 2D array with zeros
    output = [[0 for i in range(xPoints)] for j in range(yPoints)]

    # Runnig through all valid points
    for k in range(len(validPoints)):
        index = validPoints[k] # valid point index
        value = data[k] # valid point value

        # Adding point value to the 2D array
        output[getj(index)][geti(index)] = value

    return output

# Function to visualize calculation progress
# Source: https://stackoverflow.com/questions/3160699/python-progress-bar
def progressbar(it, prefix="", size=60, out=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        out.write("%s[%s%s] %i/%i\r" % (prefix, u"#"*x, "."*(size-x), j, count))
        out.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    out.write("\n")
    out.flush()

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

print("Number of valid points: ", len(validPoints), "\n") # DEBUG

# Calculating values for the matrix elements
for validIndex in progressbar(validPoints, "Computing matrix: ", 40):
    # For each valid index running through all area points (also all valid indexes)
    for index in validPoints:
        if (index == validIndex):
            # Matrix element for point (i,j)
            element = -4 * a(x(geti(index)), y(getj(index))) / (h ** 2)
        elif ((index - validIndex) == -1):
            # Matrix element for point (i-1,j)
            element = -a(x(geti(index)), y(getj(index))) / (h ** 2) - \
                      a_x(x(geti(index)), y(getj(index))) / (2 * h)
        elif ((index - validIndex) == 1):
            # Matrix element for point (i+1,j)
            element = a(x(geti(index)), y(getj(index))) / (h ** 2) + \
                      a_x(x(geti(index)), y(getj(index))) / (2 * h)
        elif ((index - validIndex) == -xPoints):
            # Matrix element for point (i,j-1)
            element = -a(x(geti(index)), y(getj(index))) / (h ** 2) - \
                      a_y(x(geti(index)), y(getj(index))) / (2 * h)
        elif ((index - validIndex) == xPoints):
            # Matrix element for point (i,j+1)
            element = a(x(geti(index)), y(getj(index))) / (h ** 2) + \
                      a_y(x(geti(index)), y(getj(index))) / (2 * h)
        else:
            # Matrix element for all other points
            element = 0
        # Adding calculated element to the matrix
        Matrix.append(element)

print("Number of matrix elements: ", len(Matrix)) # DEBUG

# Reshaping the matrix
Matrix = np.array(Matrix)
Matrix = Matrix.reshape(len(validPoints), len(validPoints))

print("Calculated matrix shape:   ", Matrix.shape, "\n") # DEBUG

############### Calculating the right side (f(x,y) vector) ###############

Right = [] # Initializing right side vector (array)
rightSidePoints = [] # Initializing right side points (array of their indexes)

# Calculating right side point indexes according to the area in which right side is defined
# (Counting from the top left corner, going right)
for i in range(xPoints):
    for j in range(yPoints):
        # Including indexes inside the area (without borders)
        if (x(i) > f_xMin and x(i) < f_xMax and y(j) > f_yMin and y(j) < f_yMax):
            index = xPoints * j + i # Point index in the 1D array
            rightSidePoints.append(int(index))

# Running through valid points, and coputing right side if it is defined in the point
for validIndex in progressbar(validPoints, "Computing right:  ", 40):
    # Checking if right side is defined in the current point
    isDefined = 0
    for rightIndex in rightSidePoints:
        if (rightIndex == validIndex):
            isDefined = 1
    # If defined, then calculating right side
    # Else, assuming it is 0
    if (isDefined):
        Right.append(f(x(geti(validIndex)), y(getj(validIndex))))
    else:
        Right.append(0.)

print("Number of right side elements: ", len(Right)) # DEBUG

############### Calculating the solution ###############



############### Plotting the matrix ###############

# Creating figure and axis
fig, axs = plt.subplots(1, 2)
fig.canvas.manager.set_window_title('Matrix')

# Black-n-white version
axs[0].spy(Matrix)

# Color map version
colorbarAxis = inset_axes(axs[1],
                   width = "5%",
                   height = "100%",
                   loc = 'lower left',
                   bbox_to_anchor = (1.05, 0., 1, 1),
                   bbox_transform = axs[1].transAxes,
                   borderpad = 0)
colorbarMap = axs[1].matshow(Matrix, cmap = 'magma')
fig.colorbar(colorbarMap, cax = colorbarAxis, orientation = "vertical")

# Titles
axs[0].set_title('Black-n-white matrix plot')
axs[1].set_title('Color map matrix plot')

############### Plotting f(x,y) ###############

# Creating x,y mesh
xGrid = np.array(range(xPoints)) * h + xMin
yGrid = np.array(range(yPoints)) * h + yMin
xMesh, yMesh = np.meshgrid(xGrid, yGrid)

# Transforming an array to a 2D array (for square-shaped area)
plotRightData = reshapeToSquare(validPoints, Right)
plotRightData = np.array(plotRightData)

# Flipping forizontally, as we used top-left corner as origin (not bottom-left)
plotRightData = np.flip(plotRightData, 0)

# Creating figure and axis
fig2, axs2 = plt.subplots()
fig2.canvas.manager.set_window_title('Function f(x,y) plot')

# Color map version
colorbarAxis = inset_axes(axs2,
                   width = "5%",
                   height = "100%",
                   loc = 'lower left',
                   bbox_to_anchor = (1.05, 0., 1, 1),
                   bbox_transform = axs2.transAxes,
                   borderpad = 0)
colorbarMap = axs2.contourf(xMesh, yMesh, plotRightData, cmap = 'magma')
fig2.colorbar(colorbarMap, cax = colorbarAxis, orientation = "vertical")
axs2.axis('square') # Forcing contourf plot to be square-shaped

# Title and labels
axs2.set_title('Function f(x,y)')
axs2.set_xlabel('x')
axs2.set_ylabel('y')

# Showing all figures
plt.show()