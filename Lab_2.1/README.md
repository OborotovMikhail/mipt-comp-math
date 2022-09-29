# Computational Math, Lab 1 (2nd semester)

## Contents

[Task](#Task)

[Calculation method](#Calculation-method)

[Program parameters](#Program-parameters)

[Program output](#Program-output)

## Task

We are looking at a system of differential equations describing the kinetics of a chemical reaction, in which three reagents are involved, designated as $A$, $B$ and $C$. The process can be written as three elementary second-order reactions.

$$ A + A \xrightarrow{k_1} B $$

$$ B + B \xrightarrow{k_2} C + B $$

$$ B + C \xrightarrow{k_3} A + C $$

Constants $k_1$, $k_2$ and $k_3$ represent the rate of the corresponding chemical reaction (i.e., the change in the concentration of the substance per unit of time). Reaction speeds differ a lot: $k_1 = 0.04$ (slow), $k_2 = 3 \cdot 10^7$ (very fast), $k_3 = 10^4$ (fast). This leads to the following system of differential equations:

$$ y_1' = - k_1 y_1 + k_3 y_2 y_3 $$

$$ y_2' = k_1 y_1 - k_3 y_2 y_3 - k_2 y_2^2 $$

$$ y_3' = k_2 y_2^2 $$

Here $y_1$ is the concentration of the substance $A$, $y_2$ is the concentration of the substance $B$, and $y_3$ is the concentration of the substance $C$. The initial concentrations are: $y_1(0) = 1$, $y_2(0) = 0$, $y_3(0) = 0$. The resulting system of differential equations is rigid because of the big difference in the rates of chemical reactions.

The task is to depict the dynamics of the concentration of substances in the time interval $t \in [0, 0.3]$.

[:arrow_up: Back to contents](#Contents)

## Calculation method



[:arrow_up: Back to contents](#Contents)

## Program parameters



[:arrow_up: Back to contents](#Contents)

## Program output

The program outputs 4 graphs as a result of the work. Those are the graphs of concentrations of substances $A$, $B$ and $C$ in the cosidered time period (starting from $t = 0$) separately and one
graph on which all concentrations are plotted together.

Individual oncentration graphs:

![alt text](https://github.com/OborotovMikhail/MIPT_CompMath/blob/main/Lab_2.1/readmeImages/imagePlot1.png? "Concentration of A")

![alt text](https://github.com/OborotovMikhail/MIPT_CompMath/blob/main/Lab_2.1/readmeImages/imagePlot2.png? "Concentration of B")

![alt text](https://github.com/OborotovMikhail/MIPT_CompMath/blob/main/Lab_2.1/readmeImages/imagePlot3.png? "Concentration of C")

All concentrations on the same graph:

![alt text](https://github.com/OborotovMikhail/MIPT_CompMath/blob/main/Lab_2.1/readmeImages/imagePlot4.png? "All concentrations on the same graph")

[:arrow_up: Back to contents](#Contents)
