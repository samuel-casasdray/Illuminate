import json
from variable import *
from Type.Line import line
from Type.Column import column
from Type.Square import square
from Type.Diagonal import diagonal
from Type.Random import random
from Type.Spread import spread
from Type.Circle import circle
from Type.Bounce import bounce
import copy
from UI.Gui import Gui
from Static import Static


class Game:
    def __init__(self):
        self.stepLevel = 0
        self.gui = None
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

    def setGui(self, gui:Gui):
        self.gui = gui

    def countNbLevel(self):
        return len(self.levels)

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

    def startGame(self, event):
        self.levelInGoing = True
        self.loop(None)
        Static.event.add(self.sendGrille, 50)

    def sendGrille(self, event):
        for i in range(0, SIZE[0]):
            for j in range(0, SIZE[1]):
                n = -1
                for k in range(0, self.nbFunc):
                    if self.grilles[k] is not None and self.grilles[k][i][j] > n:
                        n = self.grilles[k][i][j]
                self.gui.changeColor(i, j, n if n != -1 else 0)
        Static.event.add(self.sendGrille, 50)

    def loop(self, event):
        self.nbFuncDone = 0
        self.stepLevel += 1
        if self.stepLevel > self.maxStep:
            self.stepLevel = 1
        error = self.level["error"][str(self.stepLevel)]
        time1 = int(self.lunchFunc(error) * 1000)
        Static.event.add(self.loop, time1)

    def lunchFunc(self, func: str, isMulti=False, multi=0, time=0.0):
        funcs = func.split("_")
        name = funcs[0]
        try:
            n = int(funcs[1])
        except ValueError:
            n = 0
        try:
            old = int(funcs[2])
        except ValueError:
            old = 0
        match name:
            case "line":
                top = funcs[3] == "true"
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return line(n, old, top, self.replaceGrille, 0 + multi, time)
            case "column":
                left = funcs[3] == "true"
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return column(n, old, left, self.replaceGrille, 0 + multi, time)
            case "crossP":
                top = funcs[3] == "true"
                left = funcs[4] == "true"
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                time1 = line(n, old, top, self.replaceGrille, 0 + multi, time)
                time2 = column(n, old, left, self.replaceGrille, 1 + multi, time)
                return max(time1, time2)
            case "multi":
                multiFuncs = "_".join(funcs[1:]).split("__")
                self.nbFunc = sum(map(self.getNbFunc, multiFuncs))
                self.setGrilles()
                i = 0
                timeMin = float("inf")
                timeMax = 0
                for f in multiFuncs:
                    time2 = self.lunchFunc(f, True, i, time)
                    if time2 < timeMin: timeMin = time2
                    if time2 > timeMax: timeMax = time2
                    i += self.getNbFunc(f)
                return timeMin if self.maxStep == 1 else timeMax
            case "time":
                temp = self.lunchFunc("_".join(funcs[2:]), isMulti, multi, float(funcs[1]))
                return temp
            case "square":
                x = int(funcs[3])
                y = int(funcs[4])
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return square(n, old, x, y, self.replaceGrille, 0 + multi, time)
            case "diag":
                top = funcs[3] == "true"
                left = funcs[4] == "true"
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return diagonal(n, old, top, left, self.replaceGrille, 0 + multi, time)
            case "random":
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return random(n, old, self.replaceGrille, 0+multi, time)
            case "spread":
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return spread(n, old, self.replaceGrille, 0+multi, time)
            case "circle":
                x = int(funcs[3])
                y = int(funcs[4])
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return circle(n, old, x, y, self.replaceGrille, 0 + multi, time)
            case "bounce":
                x = int(funcs[3])
                y = int(funcs[4])
                size = int(funcs[5])
                angle = int(funcs[6])
                bounceN = int(funcs[7])
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return bounce(n, old, x, y, size, angle, bounceN, self.replaceGrille, 0+multi, time)
            case _:
                print("Erreur inconnu : ", func)
                return 5

    def getNbFunc(self, name):
        match name:
            case "line" | "column" | "square" | "diag" | "random" | "spread" | "circle" | "bounce":
                return 1
            case "crossP":
                return 2
            case _:
                names = name.split("_")
                if len(names) == 1: return 0
                if names[0] == "time": return self.getNbFunc(names[2])
                return self.getNbFunc(names[0])

    def setGrilles(self):
        if len(self.grilles) != self.nbFunc:
            self.grilles = [None for _ in range(0, self.nbFunc)]

    def replaceGrille(self, x, y, n, old, i):
        if len(self.grilles) <= i: return
        if self.grilles[i] is None:
            self.grilles[i] = copy.deepcopy(self.grille)
        if self.grilles[i][x][y] == old:
            self.grilles[i][x][y] = n

    def completeLevel(self):
        self.grilles = [[[3 for _ in range(0, SIZE[1])] for _ in range(0, SIZE[0])] for _ in range(0, self.nbFunc)]
        self.sendGrille(None)
        Static.event.stopAll()
        self.grilles = [None for _ in range(0, self.nbFunc)]

    def fill(self):
        pass

    def snake(self):
        pass

    def star(self):
        pass

    def bounce(self):
        pass
