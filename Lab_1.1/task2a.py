import matplotlib.pyplot as plt
import numpy as np

N = 4  # Значение по условию (обратное h)
h = 1 / N

RowLenght = N + 1  # Количество узлов по одной оси

Matrix = np.array([])  # Строка значений матрицы
Valid = np.array([])  # Массив интересующих узлов (не крайние)

# Заполняем массив интересующих узлов (т.е. НЕ крайних)
# Крайние узлы не будут рассматриваться с матрице СЛАУ (дают нулевой вклад в нее)
for i in range(RowLenght):
    for j in range(RowLenght):
        index = RowLenght * i + j  # Номер узла (строчный)
        # Включаем только НЕ крайние узлы
        if (i != 0 and j != 0 and i != (RowLenght - 1) and j != (RowLenght - 1)):
            Valid = np.append(Valid, index)

print("Интересующие узлы сетки:")
print(Valid)

# Заполняем матрицу для каждого некрайнего узла
for validIndex in Valid:
    for i in range(RowLenght - 2):
        for j in range(RowLenght - 2):
            index = RowLenght * (i + 1) + (j + 1)  # Номер узла (строчный)

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
plt.spy(Matrix)  # Визуализация матрицы СЛАУ
plt.show()