import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt

############### Parameters ###############

rate = [0.04, 30000000., 10000.] # Reaction rate (speed) vector (set as a parameter)

stepsNum = 3000 # Number of steps (set as a parameter)
timeLimit = 0.3 # Time limit in seconds (set as a parameter)

tStep = timeLimit / stepsNum # Time step

# ODE (Ordinary differential equation) system (set as a parameter)
def dy1(t, y):
    return -rate[0] * y[0] + rate[2] * y[1] * y[2]
def dy2(t, y):
    return rate[0] * y[0] - rate[2] * y[1] * y[2] - rate[1] * y[1] ** 2
def dy3(t, y):
    return rate[1] * y[1] ** 2

# Initial conditions for y (set as a parameter)
yInit = [1, 0, 0]

# Butcher matrix for Runge-Kutta method (set as a parameter)
aButcher = [[1/2, 0], 
            [-1/2, 1]]
bButcher = [-1/2, 3/2]
cButcher = [1/2, 3/2]

############### Functions ###############

# First step
def rungeKuttaFirstStep(y, tStep):
    return (1 + tStep * rate[2] * y[1] * y[2] - tStep * rate[0] * y[0] - y[0],
            0 + tStep * rate[0] * y[0] - tStep * rate[2] * y[1] * y[2] - tStep * rate[1] * y[1] ** 2 - y[1], 
            0 + tStep * rate[1] * y[1] ** 2 - y[2])

# Runge-Kutta method function
def rungeKutta(y, i, tStep, k, aButcher, bButcher, cButcher):
    # Calculating k for this step
    k[0][i][0] = dy1(tStep * i + tStep * cButcher[0],
                     y + tStep * aButcher[0][0] * k[0][i - 1][0])
    k[0][i][1] = dy1(tStep * i + tStep * cButcher[1],
                     y + tStep * aButcher[1][0] * k[0][i - 1][0] + tStep * aButcher[1][1] * k[0][i - 1][1])
    k[1][i][0] = dy2(tStep * i + tStep * cButcher[0],
                     y + tStep * aButcher[0][0] * k[1][i - 1][0])
    k[1][i][1] = dy2(tStep * i + tStep * cButcher[1],
                     y + tStep * aButcher[1][0] * k[1][i - 1][0] + tStep * aButcher[1][1] * k[1][i - 1][1])
    k[2][i][0] = dy3(tStep * i + tStep * cButcher[0],
                     y + tStep * aButcher[0][0] * k[2][i - 1][0])
    k[2][i][1] = dy3(tStep * i + tStep * cButcher[1],
                     y + tStep * aButcher[1][0] * k[2][i - 1][0] + tStep * aButcher[1][1] * k[2][i - 1][1])

    # Initializing array of sums of b_i * k_i, and calculating them
    sums = []
    for j in range(3):
        sums.append(bButcher[0] * k[j][i][0] + bButcher[1] * k[j][i][1])

    # Calculating result
    return (y[0] + tStep * (sums[0]),
            y[1] + tStep * (sums[1]),
            y[2] + tStep * (sums[2]))

############### Main calculating cycle ###############

# Initializing c with zeros (for the Runge-Kutta method)
k = []
for i in range(3):
    k.append([[0 for i in range(2)] for j in range(stepsNum)])

# Initializing y with the first step
yIntegral = []
yIntegral.append(yInit)

# First step
yFirstStep =  opt.fsolve(rungeKuttaFirstStep, yIntegral[0], tStep)
yIntegral.append(yFirstStep)

# Initializing (calculating) k for the first steps
for j in range(3):
    k[j][0] = [yIntegral[1][j], yIntegral[1][j]]

# Doing calculations with Runge-Kutta (starting with the 2nd step)
for i in range(1, stepsNum):
    yLastStep = yIntegral[-1]
    yNewStep = rungeKutta(yLastStep, i, tStep, k, aButcher, bButcher, cButcher)
    yIntegral.append(yNewStep) # Adding to the integral

############### Plots ###############

# Transposing to plot the final result
yResult = np.array(yIntegral)
yResult = np.transpose(yResult)

# Plotting
fig, axs = plt.subplots(2, 2)
fig.canvas.manager.set_window_title('Results')

axs[0, 0].plot(yResult[0], label='Concentration of A')
axs[0, 0].legend()

axs[0, 1].plot(yResult[1], 'tab:orange', label='Concentration of B')
axs[0, 1].legend()

axs[1, 0].plot(yResult[2], 'tab:green', label='Concentration of C')
axs[1, 0].legend()

axs[1, 1].plot(yResult[0], label='Concentration of A')
axs[1, 1].plot(yResult[1], 'tab:orange', label='Concentration of B')
axs[1, 1].plot(yResult[2], 'tab:green', label='Concentration of C')
axs[1, 1].legend()

for ax in axs.flat:
    ax.set(xlabel='Time, sec', ylabel='Concentration')
           
plt.show()