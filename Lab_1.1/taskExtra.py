import matplotlib.pyplot as plt
import numpy as np

################################## ПЕРВАЯ ЧАСТЬ - АЛГОРИТМ ВЫЧИСЛЕНИЯ МАТРИЦЫ СЛАУ #####################################


N = 10  # Значение по условию (обратное h)
h = 1 / N

RowLenght = N + 1  # Количество узлов по одной оси

Matrix = np.array([])  # Строка значений матрицы
Valid = np.array([])  # Массив интересующих узлов (не крайние)

# Заполняем массив интересующих узлов (НЕ крайних)
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

# Правая часть системы
Right = np.zeros(Matrix.shape[0])  # Все нули
Right[int((Right.size - 1) / 2)] = 1  # Кроме центрального узла

# Right = np.ones(Matrix.shape[0]) # Случай когда правая часть - все единицы

print("Правая часть системы:")
print(Right)

######################################## ОШИБКИ ИТЕРАЦИОННЫХ МЕТОДОВ #############################################


# Значение эпсилон
# Функции итерационных методов представленные ниже работают до достижения ошибки в эпсилон
# Используемый тип переменных - numpy.float64, имеющий 52 бита мантисы, так что значение эпсилон
# можно выбирать вплоть до 10^(-16), однако при этом будет увеличиваться кол-во итераций и время работы
eps = 10 ** (-10)


# Функция ошибки
def error(A, x, f):
    # Реализована согласно формуле ||Ax_n - f||/||f||
    Ax = np.dot(A, x)
    numerator = np.sqrt(sum((Ax[i] - f[i]) ** 2 for i in range(len(f))))
    denomerator = np.sqrt(sum((f[i]) ** 2 for i in range(len(f))))
    return numerator / denomerator


# Ниже функции ошибок итерационных методов


# SIM(tau) - simple iteration method with tau
# (реализация с семинаров)
def errSIMtau(A, f, eps):
    result = np.zeros(len(f))  # Корни
    errors = np.array([])  # Ошибки

    # Параметры метода
    I = np.eye(len(f))
    tau = 2 / (max(np.linalg.eigvals(A)) + min(np.linalg.eigvals(A)))

    currentError = error(A, result, f)  # Ошибка на нулевой итерации
    while currentError > eps:
        errors = np.append(errors, currentError)  # Добавляем ошибку в массив

        # Итерационный алгорим метода
        result = np.dot((I - np.dot(tau, A)), result) + np.dot(tau, f)

        currentError = error(A, result, f)  # Считаем новую ошибку
    return errors  # Возвращаем массив ошибок


# Jacobi
# (реализация NumPy)
def errJacobi(A, f, eps):
    result = np.zeros(len(f))  # Корни
    errors = np.array([])  # Ошибки

    # Параметры метода
    D = np.diag(A)
    R = A - np.diagflat(D)

    currentError = error(A, result, f)  # Ошибка на нулевой итерации
    while currentError > eps:
        errors = np.append(errors, currentError)  # Добавляем ошибку в массив

        # Итерационный алгорим метода
        result = (f - np.dot(R, result)) / D

        currentError = error(A, result, f)  # Считаем новую ошибку
    return errors  # Возвращаем массив ошибок


# Seidel
# (реализация с семинаров)
def errSeidel(A, f, eps):
    length = len(f)
    result = np.zeros(length)  # Корни
    errors = np.array([])  # Ошибки

    currentError = error(A, result, f)  # Ошибка на нулевой итерации
    while currentError > eps:
        errors = np.append(errors, currentError)  # Добавляем ошибку в массив

        # Итерационный алгорим метода
        temp = result
        for i in range(length):
            sum1 = sum(A[i][j] * temp[j] for j in range(i))
            sum2 = sum(A[i][j] * result[j] for j in range(i + 1, length))
            temp[i] = (f[i] - sum1 - sum2) / A[i][i]
        result = temp

        currentError = error(A, result, f)  # Считаем новую ошибку
    return errors  # Возвращаем массив ошибок


# CG - conjugate gradient (метод сопряженных градиентов)
# Реализация - https://towardsdatascience.com/complete-step-by-step-conjugate-gradient-algorithm-from-scratch-202c07fb52a8
def errCG(A, f, eps):
    result = np.zeros(len(f))  # Корни
    errors = np.array([])  # Ошибки

    # Параметры метода
    xk = result
    b = f

    rk = np.dot(A, result) - b
    pk = -rk

    num_iter = 0
    curve_x = [xk]

    currentError = error(A, xk, f)  # Ошибка на нулевой итерации
    while currentError > eps:
        errors = np.append(errors, currentError)  # Добавляем ошибку в массив

        # Итерационный алгорим метода
        apk = np.dot(A, pk)
        rkrk = np.dot(rk, rk)

        alpha = rkrk / np.dot(pk, apk)
        xk = xk + alpha * pk
        rk = rk + alpha * apk
        beta = np.dot(rk, rk) / rkrk
        pk = -rk + beta * pk

        num_iter += 1
        curve_x.append(xk)

        currentError = error(A, xk, f)  # Считаем новую ошибку
    return errors  # Возвращаем массив ошибок


##################################### ГРАФИКИ СХОДИМОСТИ РАЗЛИЧНЫХ МЕТОДОВ ###########################################

fig, ax = plt.subplots()

# Ошибки
errorsSIMtau = errSIMtau(Matrix, Right, eps)
errorsJacobi = errJacobi(Matrix, Right, eps)
errorsSeidel = errSeidel(Matrix, Right, eps)
errorsCG = errCG(Matrix, Right, eps)

# Итерации
iterationsSIMtau = np.arange(0, len(errorsSIMtau), 1)
iterationsJacobi = np.arange(0, len(errorsJacobi), 1)
iterationsSeidel = np.arange(0, len(errorsSeidel), 1)
iterationsCG = np.arange(0, len(errorsCG), 1)

# Графики
plt.plot(iterationsSIMtau, errorsSIMtau, label='SIM$_{t}$')
plt.plot(iterationsJacobi, errorsJacobi, label='Jacobi', linestyle='--')
plt.plot(iterationsSeidel, errorsSeidel, label='Seidel')
plt.plot(iterationsCG, errorsCG, label='CG')

plt.xlabel('Итерации')
plt.ylabel('$||Ax_n - f||/||f||$')
plt.legend(loc='best')
plt.grid(linestyle='--')
plt.show()

# Графики (итерации до 50)
plt.plot(iterationsSIMtau, errorsSIMtau, label='SIM$_{t}$')
plt.plot(iterationsJacobi, errorsJacobi, label='Jacobi', linestyle='--')
plt.plot(iterationsSeidel, errorsSeidel, label='Seidel')
plt.plot(iterationsCG, errorsCG, label='CG')

plt.xlabel('Итерации (до 50)')
plt.ylabel('$||Ax_n - f||/||f||$')
plt.xlim(0, 50)
plt.legend(loc='best')
plt.grid(linestyle='--')
plt.show()