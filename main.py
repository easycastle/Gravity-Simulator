from tkinter import *
import numpy as np
from random import randrange
from math import sqrt, pi

window = Tk()
window.title('n-body simulator')


canvas = Canvas(window, width=700, height=700, bg='black')
canvas.grid(row=0, column=0)

G = 0.01                                                        # gravitational constant
Bodies = []                                                     # list of Bodies

class Body:
    def __init__(self, m, x, y, V):
        self.m = m                                              # m
        self.x = x                                              # x coordination
        self.y = y                                              # y coordination
        self.P = np.array([self.x, self.y], dtype=float)        # position (x, y coordination)
        self.V = np.array(V, dtype=float)                       # velocity
        self.r = (self.m / pi) ** (1/3)                         # radius

    def Fg(self, interaction):
        if self == interaction:
            self.dV = np.array([0, 0], dtype=float)
        else:
            self.distance = sqrt((self.P[0] - interaction.P[0]) ** 2 + (self.P[1] - interaction.P[1]) ** 2)
            self.dV = np.array([0, 0], dtype=float)

            if self.distance == 0:
                self.dV = 0
            else:
                self.F = (-G * self.m * interaction.m / self.distance ** 2) * (self.P - interaction.P) / self.distance
                self.dV = self.F / self.m

                if self.distance < self.r + interaction.r + 5:
                    self.dV *= -0.5

        self.V += self.dV

        if self.P[0] < 10 + self.r:
            self.V[0] *= -0.9
            self.P[0] += 1
        if self.P[0] > 698 - self.r:
            self.V[0] *= -0.9
            self.P[0] -= 1
        if self.P[1] < 10 + self.r:
            self.V[1] *= -0.9
            self.P[1] += 1
        if self.P[1] > 698 - self.r:
            self.V[1] *= -0.9
            self.P[1] -= 1


B = 2

for i in range(B):
    Bodies.append(Body(randrange(100, 1000), randrange(50, 650), randrange(50, 650), [0.005, 0.001]))

T = 0
Tx = True
while Tx == True:
    T += 1

    canvas.delete('all')

    for Body1 in Bodies:
        for Body2 in Bodies:
            Body1.Fg(Body2)
        Body1.P += Body2.V

        if Body1.P[0] < 5:
            Body1.V[0] *= -0.5
        if Body1.P[0] > 695:
            Body1.V[0] *= -0.5

        if Body1.P[1] < 5:
            Body1.V[1] *= -0.5
        if Body1.P[1] > 695:
            Body1.V[1] *= -0.5

        canvas.create_oval(Body1.P[0] - Body1.r, Body1.P[1] - Body1.r, Body1.P[0] + Body1.r, Body1.P[1] + Body1.r, fill='skyblue')

    canvas.update()

    if T == 100000:
        Tx = False

window.mainloop()