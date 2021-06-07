from tkinter import *
import tkinter.messagebox as msgbox
import keyboard

import numpy as np
from random import randrange
from math import sqrt, pi

window = Tk()
window.title('n-body simulator')


t = 0
time = StringVar()

timeLabel = Label(window, textvariable=time, height=3)
timeLabel.pack(side='top', fill='x')


space = Canvas(window, width=700, height=700, bg='black')
space.pack()

G = 0.001                                                        # gravitational constant
Bodies = []                                                     # list of Bodies


class Body:
    def __init__(self, m, P, V):
        self.m = m                                              # m
        self.P = np.array(P, dtype=float)                       # position (x, y coordination)
        self.Px = P[0]                                          # x coordination
        self.Py = P[1]                                          # y coordination
        self.V = np.array(V, dtype=float)                       # velocity
        self.Vx = V[0]                                          # x velocity
        self.Vy = V[1]                                          # y velocity
        self.r = (self.m / pi) ** (1/3)                         # radius

    def newton(self, interaction):
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

        if self.P[0] < 2 + self.r:
            self.V[0] *= -0.9
            self.P[0] += 1
        if self.P[0] > 698 - self.r:
            self.V[0] *= -0.9
            self.P[0] -= 1
        if self.P[1] < 2 + self.r:
            self.V[1] *= -0.9
            self.P[1] += 1
        if self.P[1] > 698 - self.r:
            self.V[1] *= -0.9
            self.P[1] -= 1


number = 20

for i in range(number):
    Bodies.append(Body(randrange(500, 1000), [randrange(50, 650), randrange(50, 650)], [randrange(-1, 1)/100, randrange(-1, 1)/100]))

while t != -1:
    t += 1
    time.set('T : {0} h'.format(t))

    space.delete('all')

    for Body1 in Bodies:
        for Body2 in Bodies:
            Body1.newton(Body2)
            Body1.P += Body1.V

        if Body1.P[0] < 5:
            Body1.V[0] *= -0.5
        if Body1.P[0] > 695:
            Body1.V[0] *= -0.5

        if Body1.P[1] < 5:
            Body1.V[1] *= -0.5
        if Body1.P[1] > 695:
            Body1.V[1] *= -0.5

        space.create_oval(Body1.P[0] - Body1.r, Body1.P[1] - Body1.r, Body1.P[0] + Body1.r, Body1.P[1] + Body1.r, fill='skyblue')

    space.update()

window.quit()

window.mainloop()