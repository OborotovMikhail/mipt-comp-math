# Computational Math, Lab 1 (2nd semester)

## Contents

[Task](#Task)

[Calculation method](#Calculation-method)

[Program parameters](#Program-parameters)

[Program output](#Program-output)

## Task

We are looking at a system of differential equations describing the kinetics of a chemical reaction, in which three reagents are involved, designated as $A$, $B$ and $C$. The process can be written as three elementary second-order reactions.

$$ A + A \xleftarrow{k_1} B $$

$$ B + B \xleftarrow{k_2} C + B $$

$$ B + C \xleftarrow{k_3} A + C $$

Constants $k_1$, $k_2$ and $k_3$ denote the rate of the corresponding chemical reaction (i.e., the change in the concentration of the substance per unit of time). The reaction differ a lot: $k_1 = 0.04$ (slow), $k_2 = 3 \cdot 10^7$ (very fast), $k_3 = 10^4$ (fast). This leads to the following system of differential equations:

$$ y_1' = - k_1 y_1 + k_3 y_2 y_3 $$

$$ y_2' = k_1 y_1 - k_3 y_2 y_3 - k_2 y_2^2 $$

$$ y_3' = k_2 y_2^2 $$

Here $y_1$ is the concentration of the substance $A$, $y_2$ is the concentration of the substance $B$, and $y_3$ is the concentration of the substance $C$. The initial concentrations are: $y_1(0) = 1$, $y_2(0) = 0$, $y_3(0) = 0$. The resulting system of differential equations is rigid because of the big difference in the rates of chemical reactions.

[:arrow_up: Back to contents](#Contents)

## Calculation method



[:arrow_up: Back to contents](#Contents)

## Program parameters



[:arrow_up: Back to contents](#Contents)

## Program output



[:arrow_up: Back to contents](#Contents)
