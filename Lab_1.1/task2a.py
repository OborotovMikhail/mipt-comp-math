import matplotlib.pyplot as plt
import numpy as np

N = 4 # Number of steps (set as a parameter)
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

# Заполняем матрицу для каждого некрайнего узла
# Filling in a matrix
for validIndex in Valid:
    for i in range(RowLenght - 2):
        for j in range(RowLenght - 2):
            index = RowLenght * (i + 1) + (j + 1) # Номер узла (строчный)

            if index == validIndex:
                # Значение в самом узле (центр креста)
                Matrix = np.append(Matrix, 4)
            elif abs(validIndex - index) == 1 or abs(validIndex - index) == RowLenght:
                # Соседние элементы и элементы, отличающиеся на длину сетки некрайних узлов
                # (концы креста)
                Matrix = np.append(Matrix, -1)
            else:
                # Остальные значения = 0
                Matrix = np.append(Matrix, 0)

# Преобразование строки в матрицу
Matrix = Matrix.reshape(len(Valid), len(Valid))
Matrix = Matrix / h / h  # учитываем h

print("Получаемая матрица СЛАУ:")
print(Matrix)

plt.spy(Matrix) # Визуализация матрицы СЛАУ
plt.show()