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


############### Calculating the matrix ###############

Matrix = np.array([]) # Initializing matrix a 1D array for now
validPoints = np.array([]) # Initializing valid points (array of their indexes)

# Calculating valid point indexes according to our area
# Border points are not included, only those inside the area
# (Counting from the top left corner, going right)
for i in range(xPoints):
    for j in range(yPoints):
        # Including indexes inside the area
        if (i != 0 and j != 0 and i != (xPoints - 1) and j != (yPoints - 1)):
            if (i < ((xPoints - 1) / 2) or j < ((yPoints - 1) / 2)):
                index = xPoints * j + i # Point index in the 1D array
                validPoints = np.append(validPoints, index)

# debug
print(len(validPoints))

# Calculating values for the matrix elements
for validIndex in validPoints :
    for i in range(xPoints - 2) :
        for j in range(yPoints - 2) :
            index = RowLenght * (i + 1) + (j + 1) # Point index in the 1D array
            
            if index == validIndex :
                # Значение в самом узле (центр креста)
                Matrix = np.append(Matrix, 4)
            elif abs(validIndex - index) == 1 or abs(validIndex - index) == RowLenght :
                # Соседние элементы и элементы, отличающиеся на длину сетки некрайних узлов
                # (концы креста)
                Matrix = np.append(Matrix, -1)
            else :
                # Остальные значения = 0
                Matrix = np.append(Matrix, 0)
