import matplotlib.pyplot as plt
import numpy as np

h = 1 / 4 # Grid step (set as a parameter)

# RHS (right-hand side) of the SLE (set as a parameter)
Right = np.array([1,1,1,1,1,1,1,1,1])

# SLE (system of linear equations) matrix
# Calculated analytically for further comparison with the algorithmic implementation
Matrix = np.array([[ 4,-1, 0,-1, 0, 0, 0, 0, 0],
                   [-1, 4,-1, 0,-1, 0, 0, 0, 0],
                   [ 0,-1, 4, 0, 0,-1, 0, 0, 0],
                   [-1, 0, 0, 4,-1, 0,-1, 0, 0],
                   [ 0,-1, 0,-1, 4,-1, 0,-1, 0],
                   [ 0, 0,-1, 0,-1, 4, 0, 0,-1],
                   [ 0, 0, 0,-1, 0, 0, 4,-1, 0],
                   [ 0, 0, 0, 0,-1, 0,-1, 4,-1],
                   [ 0, 0, 0, 0, 0,-1, 0,-1, 4]])
Matrix = Matrix / h / h # Taking h (grid step) into account

# Printing SLE matrix
print("\nSLE matrix:")
print(Matrix)

# Plotting SLE matrix visualization
figMatrix, axMatrix = plt.subplots(1, 1)
figMatrix.canvas.manager.set_window_title('Theoretical SLE matrix visualization')
axMatrix.set_title('Theoretical SLE matrix visualization')
axMatrix.spy(Matrix)

# Printing RHS of the SLE
print("\nRHS of the SLE:")
print(Right)

# Solution (using a standart method)
Solution = np.linalg.solve(Matrix, Right)
print("\nSLE solution:")
print(Solution)

# Showing all figures
plt.show()