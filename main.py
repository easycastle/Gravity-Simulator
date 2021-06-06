from tkinter import *
import tkinter.messagebox as msgbox
import keyboard

import numpy as np
from random import randrange
from math import sqrt, pi

window = Tk()
window.title('n-body simulator')


t = 0

def endSpace():
    global t

    msgbox.showinfo('중지', '우주가 {0}일 동안 진행되었습니다.'.format(t))
    t = -1


space = Canvas(window, width=700, height=700, bg='black')
space.pack()

quitBtn = Button(window, text='닫기', width=20, height=2, command=endSpace)
quitBtn.pack(side='right')

G = 0.01                                                        # gravitational constant
Bodies = []                                                     # list of Bodies


class Body:
    def __init__(self, m, P, V):
        self.m = m                                              # m
        self.P = np.array(P, dtype=float)                       # position (x, y coordination)
        self.V = np.array(V, dtype=float)                       # velocity
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


number = 25

for i in range(number):
    Bodies.append(Body(randrange(100, 1000), [randrange(50, 650), randrange(50, 650)], [0, 0]))

while t != -1:
    t += 1

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

window.mainloop()