import matplotlib.pyplot as plt
import numpy as np

h = 1 / 4 # Шаг сетки (по условию)

# Матрица СЛАУ
# Посчитана теоретически для дальнейшего сравнения с алгоритмической реализацией
Matrix = np.array([[4,-1,0,-1,0,0,0,0,0],
                   [-1,4,-1,0,-1,0,0,0,0],
                   [0,-1,4,0,0,-1,0,0,0],
                   [-1,0,0,4,-1,0,-1,0,0],
                   [0,-1,0,-1,4,-1,0,-1,0],
                   [0,0,-1,0,-1,4,0,0,-1],
                   [0,0,0,-1,0,0,4,-1,0],
                   [0,0,0,0,-1,0,-1,4,-1],
                   [0,0,0,0,0,-1,0,-1,4]])
Matrix = Matrix / h / h # учитываем h

print("Матрица СЛАУ:")
print(Matrix)
plt.spy(Matrix) # Визуализация матрицы СЛАУ
plt.show()

# Правая часть системы
Right = np.array([1,1,1,1,1,1,1,1,1])

print("Правая часть системы:")
print(Right)

# Решение системы (библиотечной функцией)
Solution = np.linalg.solve(Matrix, Right)
print("Решение:")
print(Solution)