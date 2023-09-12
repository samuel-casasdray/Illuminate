import json
import time

import customtkinter
from variable import *
from Type.Line import line
from Type.Column import column
from Type.Square import square
import copy
import guizero


class Game:
    def __init__(self):
        self.stepLevel = 0
        self.func = None
        self.maxStep = 0
        self.level = None
        self.grille = []
        self.grilles = []
        self.nbFunc = 0
        self.nbFuncDone = 0
        f = open("levels.json")
        self.levels = json.load(f)
        f.close()
        self.levelInGoing = False

    def resetGrille(self):
        self.grille = []
        for i in range(0, SIZE[0]):
            row = []
            for j in range(0, SIZE[1]):
                row.append(0)
            self.grille.append(row)

    def loadLevel(self, level):
        self.level = self.levels[level]
        self.resetGrille()
        for loc in self.level["safe"]:
            self.grille[loc[0]][loc[1]] = 4
        for loc in self.level["step"]:
            self.grille[loc[0]][loc[1]] = 2
        for i, value in self.level["border"].items():
            n = int(i)
            for border in value:
                x0 = border[0]
                x1 = border[1]
                y0 = border[2]
                y1 = border[3]
                for j in range(x0, x1):
                    self.grille[j][y0] = n
                    self.grille[j][y1] = n
                for j in range(y0, y1):
                    self.grille[y0][j] = n
                    self.grille[y1][j] = n
        self.maxStep = len(self.level["error"])
        self.stepLevel = 0

    def stopGame(self):
        self.levelInGoing = False

    def startGame(self, app: guizero.App):
        self.levelInGoing = True
        self.loop(app)
        app.repeat(50, self.sendGrille, [app])

    def sendGrille(self, app: guizero.App):
        for i in range(0, SIZE[0]):
            for j in range(0, SIZE[1]):
                n = -1
                for k in range(0, self.nbFunc):
                    if self.grilles[k] is not None and self.grilles[k][i][j] > n:
                        n = self.grilles[k][i][j]
                self.func(i, j, n if n != -1 else 0)

    def loop(self, app: guizero.App):
        self.nbFuncDone = 0
        self.stepLevel += 1
        if self.stepLevel > self.maxStep:
            self.stepLevel = 1
        error = self.level["error"][str(self.stepLevel)]
        time1 = int(self.lunchFunc(app, error) * 1000)
        app.after(time1, self.loop, [app])

    def lunchFunc(self, app: guizero.App, func, isMulti=False, multi=0, time=0.0):
        funcs = func.split("_")
        name = funcs[0]
        try: n = int(funcs[1])
        except ValueError: n = 0
        try: old = int(funcs[2])
        except ValueError: old = 0
        match name:
            case "line":
                top = funcs[3] == "true"
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return line(app, n, old, top, self.replaceGrille, 0 + multi, time)
            case "column":
                left = funcs[3] == "true"
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return column(app, n, old, left, self.replaceGrille, 0 + multi, time)
            case "crossP":
                top = funcs[3] == "true"
                left = funcs[4] == "true"
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                time1 = line(app, n, old, top, self.replaceGrille, 0 + multi, time)
                time2 = column(app, n, old, left, self.replaceGrille, 1 + multi, time)
                return max(time1, time2)
            case "multi":
                multiFuncs = "_".join(funcs[1:]).split("__")
                self.nbFunc = sum(map(self.getNbFunc, multiFuncs))
                self.setGrilles()
                i = 0
                timeMin = float("inf")
                timeMax = 0
                for f in multiFuncs:
                    time2 = self.lunchFunc(app, f, True, i, time)
                    if time2 < timeMin: timeMin = time2
                    if time2 > timeMax: timeMax = time2
                    i += self.getNbFunc(f)
                return timeMin if self.maxStep == 1 else timeMax
            case "time":
                temp = self.lunchFunc(app, "_".join(funcs[2:]), isMulti, multi, float(funcs[1]))
                return temp
            case "square":
                x = int(funcs[3])
                y = int(funcs[4])
                print(x, y)
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return square(app, n, old, x, y, self.replaceGrille, 0 + multi, time)
            case _:
                print("Erreur inconnu : ", func)
                return 5

    def getNbFunc(self, name):
        match name:
            case "line" | "column" | "square":
                return 1
            case "crossP":
                return 2
            case _:
                names = name.split("_")
                if len(names) == 1: return 0
                if names[0] == "time": return self.getNbFunc(names[2])
                return self.getNbFunc(names[0])

    def setFunc(self, func):
        self.func = func

    def setGrilles(self):
        if len(self.grilles) != self.nbFunc:
            self.grilles = [None for _ in range(0, self.nbFunc)]

    def replaceGrille(self, x, y, n, old, i):
        if len(self.grilles) <= i: return
        if self.grilles[i] is None:
            self.grilles[i] = copy.deepcopy(self.grille)
        if self.grilles[i][x][y] == old:
            self.grilles[i][x][y] = n


    def diagR(self):
        pass

    def diagC(self):
        pass

    def fill(self):
        pass

    def crossT(self):
        pass

    def circle(self):
        pass

    def square(self):
        pass

    def snake(self):
        pass
