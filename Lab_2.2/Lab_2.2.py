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

# Area in which right side (f(x,y) function) is defined (set as a parameter)
f_xMin = xMin - xMin / 4
f_xMax = xMin / 4
f_yMin = yMax / 4
f_yMax = yMax - yMax / 4

# Desired error of the solution (set as a parameter)
eps = 10 ** (-10)

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

# Error calculation function
def error(A, x, f) :
    # Calculating error as ||Ax_n - f|| / ||f||
    Ax = np.dot(A, x)
    numerator = np.sqrt(sum( (Ax[i] - f[i]) ** 2 for i in range(len(f)) ))
    denomerator = np.sqrt(sum( (f[i]) ** 2 for i in range(len(f)) ))
    return numerator / denomerator

############### Iterable solver method functions ###############

# SIM(tau) - simple iteration method with tau
def SIMtau(A, f, eps) :
    solution = np.zeros(len(f)) # Solutions
    errors = np.array([]) # Errors
    
    # Parameters for this method
    I = np.eye(len(f))
    tau = 2 / (max(np.linalg.eigvals(A)) + min(np.linalg.eigvals(A)))
    
    currentError = error(A, solution, f) # First step error
    while currentError > eps :
        errors = np.append(errors, currentError) # Adding error to the array
        
        # Iterable method
        solution = np.dot((I - np.dot(tau, A)), solution) + np.dot(tau, f)
        
        currentError = error(A, solution, f) # Calculating new error
    
    return solution, errors

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

Solution = np.linalg.solve(Matrix, Right)

############### Plotting the matrix ###############

# Creating figure and axis
figMatrix, axMatrix = plt.subplots(1, 2)
figMatrix.canvas.manager.set_window_title('Matrix')

# Black-n-white version
axMatrix[0].spy(Matrix)

# Color map version
caxMatrix = inset_axes(axMatrix[1],
                   width = "5%",
                   height = "100%",
                   loc = 'lower left',
                   bbox_to_anchor = (1.05, 0., 1, 1),
                   bbox_transform = axMatrix[1].transAxes,
                   borderpad = 0)
cmapMatrix = axMatrix[1].matshow(Matrix, cmap = 'plasma')
figMatrix.colorbar(cmapMatrix, cax = caxMatrix, orientation = "vertical")

# Titles
axMatrix[0].set_title('Black-n-white matrix plot')
axMatrix[1].set_title('Color map matrix plot')

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
figFunc, axFunc = plt.subplots()
figFunc.canvas.manager.set_window_title('Function f(x,y) plot')

# Color map version
caxFunc = inset_axes(axFunc,
                   width = "5%",
                   height = "100%",
                   loc = 'lower left',
                   bbox_to_anchor = (1.05, 0., 1, 1),
                   bbox_transform = axFunc.transAxes,
                   borderpad = 0)
cmapFunc = axFunc.contourf(xMesh, yMesh, plotRightData, cmap = 'plasma')
figFunc.colorbar(cmapFunc, cax = caxFunc, orientation = "vertical")
axFunc.axis('square') # Forcing contourf plot to be square-shaped

# Title and labels
axFunc.set_title('Function f(x,y)')
axFunc.set_xlabel('x')
axFunc.set_ylabel('y')

############### Plotting solution ###############

# Transforming an array to a 2D array (for square-shaped area)
plotSolution = reshapeToSquare(validPoints, Solution)
plotSolution = np.array(plotSolution)

# Flipping forizontally, as we used top-left corner as origin (not bottom-left)
plotSolution = np.flip(plotSolution, 0)

# Creating figure and axis
figSolution, axSolution = plt.subplots()
figSolution.canvas.manager.set_window_title('Solution plot')

# Color map version
caxSolution = inset_axes(axSolution,
                   width = "5%",
                   height = "100%",
                   loc = 'lower left',
                   bbox_to_anchor = (1.05, 0., 1, 1),
                   bbox_transform = axSolution.transAxes,
                   borderpad = 0)
cmapSolution = axSolution.contourf(xMesh, yMesh, plotSolution, cmap = 'plasma')
figSolution.colorbar(cmapSolution, cax = caxSolution, orientation = "vertical")
axSolution.axis('square') # Forcing contourf plot to be square-shaped

# Title and labels
axSolution.set_title('Solution')
axSolution.set_xlabel('x')
axSolution.set_ylabel('y')

# Showing all figures
plt.show()