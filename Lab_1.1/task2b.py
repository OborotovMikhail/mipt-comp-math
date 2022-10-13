import matplotlib.pyplot as plt
import numpy as np

N = 20 # Number of steps (set as a parameter)
h = 1 / N # Grid step

RowLenght = N + 1 # Number of nodes on 1 axis

Matrix = np.array([]) # SLE matrix values (as a string, not a matrix)
Valid = np.array([]) # Array of nodes of interest (all except border nodes)

# Filling an array of valid nodes (the nodes of interest)
# Border nodes are not of interest as they have a zero contribution to the SLE matrix values
for i in range(RowLenght):
    for j in range(RowLenght):
        index = RowLenght * i + j # Node index
        # Including all nodes except border ones
        if (i != 0 and j != 0 and i != (RowLenght - 1) and j != (RowLenght - 1)):
            Valid = np.append(Valid, index)

# Printing idexes of nodes of interest
print("\nNodes of interest:")
print(Valid)

# Calculating matrix values for each node
for validIndex in Valid:
    for i in range(RowLenght - 2):
        for j in range(RowLenght - 2):
            index = RowLenght * (i + 1) + (j + 1) # Node index

            if index == validIndex:
                # Value in the node itself (center of the cross)
                Matrix = np.append(Matrix, 4)
            elif abs(validIndex - index) == 1 or abs(validIndex - index) == RowLenght:
                # Adjacent nodes and nodes differing by the length of the grid
                # (ends of the cross)
                Matrix = np.append(Matrix, -1)
            else:
                # All other values are zero
                Matrix = np.append(Matrix, 0)

Matrix = Matrix.reshape(len(Valid), len(Valid)) # Reshaping to a matrix
Matrix = Matrix / h / h # Taking h (grid step) into account

# Printing SLE matrix
print("\nCalculated SLE matrix:")
print(Matrix)

# Plotting SLE matrix visualization
figMatrix, axMatrix = plt.subplots(1, 1)
figMatrix.canvas.manager.set_window_title('Calculated SLE matrix visualization')
axMatrix.set_title('Calculated SLE matrix visualization')
axMatrix.spy(Matrix)

# RHS (right-hand side) of the SLE (set as a parameter)
Right = np.zeros(Matrix.shape[0]) # All zeros
Right[int((Right.size - 1) / 2)] = 1 # Except the center node

# Printing RHS of the SLE
print("\nRHS of the SLE:")
print(Right)

# Solution (using a standart method)
Solution = np.linalg.solve(Matrix, Right)

# Printing solution
print("\nSLE solution:")
print(Solution)

# Plotting the solution
ReshapedSolutionLen = int(np.sqrt(Solution.size)) # Reshaped solution length
ReshapedSolution = Solution.reshape(ReshapedSolutionLen, ReshapedSolutionLen) # Reshaping solution
Pad = np.pad(ReshapedSolution, (1, 1), mode='constant') # Creating pad (for the plot)
Colormap = plt.get_cmap('jet') # Colormap
figSolution, axSolution = plt.subplots(1, 1)
figSolution.canvas.manager.set_window_title('Solution plot')
axSolution.set_title('Solution plot')
Plot = axSolution.imshow(Pad, Colormap, aspect='equal', vmin=0, extent=(0, 1, 0, 1), interpolation='gaussian')
figSolution.colorbar(Plot, ax=axSolution)
plt.grid(linestyle='--')

# Showing all figures
plt.show()