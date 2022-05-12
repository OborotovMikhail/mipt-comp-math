import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt

k = np.array([0.04, 30000000, 10000]) # Reaction rate (speed) vector (set as a parameter)

stepsNum = 1000 # Number of steps (set as a parameter)
timeLimit = 0.3 # Time limit in seconds (set as a parameter)

tStep = timeLimit / stepsNum # Time step

# ODE (Ordinary differential equation) system (set as a parameter)
def dy1(y):
    y1, y2, y3 = y
    return -k[0] * y1 + k[2] * y2 * y3
def dy2(y):
    y1, y2, y3 = y
    return k[0] * y1 - k[2] * y2 * y3 - k[1] * y2 ** 2
def dy3(y):
    y1, y2, y3 = y
    return k[1] * y2 ** 2

# Initial conditions for y (set as a parameter)
yInit = [1, 0, 0]

# Butcher matrix for Runge-Kutta method (set as a parameter)
aButcher = [[1/2, 0],
            [-1/2, 2]]
bButcher = [1, 0]
cButcher = [1/2, 3/2]

# First step
def rungeKuttaFirstStep(y):
    ySolution = [1 + tStep * k[2] * y[1] * y[2] - tStep * k[0] * y[0] - y[0],
                 0 + tStep * k[0] * y[0] - tStep * k[2] * y[1] * y[2] - tStep * k[1] * y[1] ** 2 - y[1], 
                 0 + tStep * k[1] * y[1] ** 2 - y[2]]
    return ySolution

# Runge-Kutta method function
def rungeKutta(value, i, tStep, k, c, aButcher, bButcher, cButcher):
    y = np.array(value) # Input value (previous step y)

    a = aButcher
    b = bButcher

    c[0][i][0] = dy1(y + tStep * a[0][0] * c[0][i - 1][0])
    c[0][i][1] = dy1(y + tStep * a[1][0] * c[0][i - 1][0] + tStep * a[1][1] * c[0][i - 1][1])
    c[1][i][0] = dy2(y + tStep * a[0][0] * c[1][i - 1][0])
    c[1][i][1] = dy2(y + tStep * a[1][0] * c[1][i - 1][0] + tStep * a[1][1] * c[1][i - 1][1])
    c[2][i][0] = dy3(y + tStep * a[0][0] * c[2][i - 1][0])
    c[2][i][1] = dy3(y + tStep * a[1][0] * c[2][i - 1][0] + tStep * a[1][1] * c[2][i - 1][1])

    sums = [] # Initializing array of sums of b_i * c_i

    for j in range(3):
        sums.append(b[0]*C[j][i][0] + b[1] * C[j][i][1])

    # Calculating result
    ySolution = [y[0] + tStep * (sums[0]),
                 y[1] + tStep * (sums[1]),
                 y[2] + tStep * (sums[2])]
    return ySolution

# Initializing c with zeros (for the Runge-Kutta method)
c = []
for i in range(3):
    c.append([[0 for i in range(2)] for j in range(stepsNum)])

####### Main calculating cycle #######

# Initializing y with the first step
yIntegral = []
yIntegral.append(yInit)
print(yIntegral)

# First step
yFirstStep1, yFirstStep2, yFirstStep3 = opt.fsolve(rungeKuttaFirstStep, yInit)
yFirstStep = [yFirstStep1, yFirstStep2, yFirstStep3]
yIntegral.append(yFirstStep)

print(yIntegral)

# Initializing (calculating) for the first steps
#for j in range(3):
#    c[j][0] = [yIntegral[j][1] - yIntegral[j][0], yIntegral[j][1] - yIntegral[j][0]]

c[0][0] = [yIntegral[0][1] - yIntegral[0][0], yIntegral[0][1] - yIntegral[0][0]]
c[1][0] = [yIntegral[1][1] - yIntegral[1][0],yIntegral[1][1] - yIntegral[1][0]]
c[2][0] = [yIntegral[2][1] - yIntegral[2][0],yIntegral[2][1] - yIntegral[2][0]]

# Doing calculations with Runge-Kutta
for i in range(1, stepsNum):
    y = yIntegral[-1]
    ySolution = rungeKutta(y, i, tStep, k, c, aButcher, bButcher, cButcher)
    yIntegral.append(ySolution) # Adding to the integral

####### Plots #######

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(yIntegral[0])
axs[0, 0].set_title('Axis [0, 0]')
axs[0, 1].plot(yIntegral[1], 'tab:orange')
axs[0, 1].set_title('Axis [0, 1]')
axs[1, 0].plot(yIntegral[2], 'tab:green')
axs[1, 0].set_title('Axis [1, 0]')
axs[1, 1].plot(yIntegral[2], 'tab:red')
axs[1, 1].set_title('Axis [1, 1]')

for ax in axs.flat:
    ax.set(xlabel='x-label', ylabel='y-label')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()
