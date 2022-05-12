import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

k = np.array([0.04, 30000000, 10000]) # Reaction speed vector (set as a parameter)

stepsNum = 1000 # Number of steps (set as a parameter)
timeLimit = 0.3 # Time limit in seconds (set as a parameter)

tStep = timeLimit / stepsNum # Time step

# ODE (Ordinary differential equation) system (set as a parameter)
def dy1(y1, y2, y3):
  return -k[0] * y1 + k[2] * y2 * y3
def dy2(y1, y2, y3):
  return k[0] * y1 - k[2] * y2 * y3 - k[1] * y2 ** 2
def dy3(y1, y2, y3):
  return k[1] * y2 ** 2

# Conditions for y (set as a parameter)
yInit = np.array([1, 0, 0])

# Butcher matrix for Runge-Kutta method (set as a parameter)
Butcher = np.matrix([[1/2, 1/2, 0],
                     [3/2, -1/2, 2],
                     [0, 1, 0]])

# First step
def rungeKuttaFirstStep(value):
    y = np.array()
    y = value
    return (1 + tStep * k[3] * y2 * y3 - tStep * k[1] * y1 - y1,
            0 + tStep * k[1] * y1 - tStep * k[3] * y2 * y3 - tStep * k[2] * y2 ** 2 - y2, 
            0 + tStep * k[2] * y2 ** 2 - y3)

# Runge-Kutta method function
def rungeKutta(value, i):
    y = np.array()
    y = value
    return ySolution



# Main calculating cycle
for i in range(stepsNum):
    ySolution = np.array()
    ySolution = rungeKutta(y, i)


