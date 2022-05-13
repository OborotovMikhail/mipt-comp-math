import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt

rate = [0.04, 30000000., 10000.] # Reaction rate (speed) vector (set as a parameter)

stepsNum = 3000 # Number of steps (set as a parameter)
timeLimit = 0.3 # Time limit in seconds (set as a parameter)

t = timeLimit / stepsNum # Time step

# ODE (Ordinary differential equation) system (set as a parameter)
def dy1(y):
    return -rate[0] * y[0] + rate[2] * y[1] * y[2]
def dy2(y):
    return rate[0] * y[0] - rate[2] * y[1] * y[2] - rate[1] * y[1] ** 2
def dy3(y):
    return rate[1] * y[1] ** 2

# Initial conditions for y (set as a parameter)
yInit = [1, 0, 0]

# Butcher matrix for Runge-Kutta method (set as a parameter)
a = [[1/2, 0], 
     [-1/2, 1]]
b = [-1/2, 3/2]
cButch = [1/2, 3/2]

# First step
def rungeKuttaFirstStep(y):
    return (1 + t * rate[2] * y[1] * y[2] - t * rate[0] * y[0] - y[0],
            0 + t * rate[0] * y[0] - t * rate[2] * y[1] * y[2] - t * rate[1] * y[1] ** 2 - y[1], 
            0 + t * rate[1] * y[1] ** 2 - y[2])

# Runge-Kutta method function
def rungeKutta(y, i, t, c, a, b, cButch):

    c[0][i][0] = dy1(y + t * a[0][0] * c[0][i - 1][0])
    c[0][i][1] = dy1(y + t * a[1][0] * c[0][i - 1][0] + t * a[1][1] * c[0][i - 1][1])
    c[1][i][0] = dy2(y + t * a[0][0] * c[1][i - 1][0])
    c[1][i][1] = dy2(y + t * a[1][0] * c[1][i - 1][0] + t * a[1][1] * c[1][i - 1][1])
    c[2][i][0] = dy3(y + t * a[0][0] * c[2][i - 1][0])
    c[2][i][1] = dy3(y + t * a[1][0] * c[2][i - 1][0] + t * a[1][1] * c[2][i - 1][1])

    sums = [] # Initializing array of sums of b_i * c_i

    for j in range(3):
        sums.append(b[0] * c[j][i][0] + b[1] * c[j][i][1])

    # Calculating result
    return (y[0] + t * (sums[0]),
            y[1] + t * (sums[1]),
            y[2] + t * (sums[2]))

# Initializing c with zeros (for the Runge-Kutta method)
c = []
for i in range(3):
    c.append([[0 for i in range(2)] for j in range(stepsNum)])

####### Main calculating cycle #######

# Initializing y with the first step
yIntegral = []
yIntegral.append(yInit)

# First step
yFirstStep =  opt.fsolve(rungeKuttaFirstStep, yIntegral[0])
yIntegral.append(yFirstStep)

# Initializing (calculating) for the first steps
for j in range(3):
    c[j][0] = [yIntegral[1][j], yIntegral[1][j]]

#c[0][0] = [yIntegral[1][0] - yIntegral[0][0], yIntegral[1][0] - yIntegral[0][0]]
#c[1][0] = [yIntegral[1][1] - yIntegral[0][1], yIntegral[1][1] - yIntegral[0][1]]
#c[2][0] = [yIntegral[1][2] - yIntegral[0][2], yIntegral[1][2] - yIntegral[0][2]]

# Doing calculations with Runge-Kutta
for i in range(1, stepsNum):
    yNew = yIntegral[-1]
    ySolution = rungeKutta(yNew, i, t, c, a, b, cButch)
    yIntegral.append(ySolution) # Adding to the integral

# Transposing to get the final result
yResult = np.array(yIntegral)
yResult = np.transpose(yResult)

####### Plots #######

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(yResult[0])
axs[0, 0].set_title('Axis [0, 0]')
axs[0, 1].plot(yResult[1], 'tab:orange')
axs[0, 1].set_title('Axis [0, 1]')
axs[1, 0].plot(yResult[2], 'tab:green')
axs[1, 0].set_title('Axis [1, 0]')
axs[1, 1].plot(yResult[2], 'tab:red')
axs[1, 1].set_title('Axis [1, 1]')

for ax in axs.flat:
    ax.set(xlabel='x-label', ylabel='y-label')

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

plt.show()
