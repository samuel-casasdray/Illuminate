import json
import customtkinter
from variable import *
from Type.Line import line
from Type.Column import column
import copy


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

    def startGame(self, app: customtkinter.CTkBaseClass):
        self.levelInGoing = True
        self.loop(app)

    def loop(self, app: customtkinter.CTkBaseClass):
        self.nbFuncDone = 0
        self.stepLevel += 1
        if self.stepLevel > self.maxStep:
            self.stepLevel = 1
        error = self.level["error"][str(self.stepLevel)]
        app.after(int(self.lunchFunc(app, error) * 1000), self.loop, app)

    def lunchFunc(self, app: customtkinter.CTkBaseClass, func, isMulti=False, multi=0, time=0):
        print(func)
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
                return line(app, n, old, top, self.replaceGrille, self.doneReplace, 0 + multi, time)
            case "column":
                left = funcs[3] == "true"
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                return column(app, n, old, left, self.replaceGrille, self.doneReplace, 0 + multi, time)
            case "crossP":
                top = funcs[3] == "true"
                left = funcs[4] == "true"
                if not isMulti:
                    self.nbFunc = self.getNbFunc(name)
                    self.setGrilles()
                time1 = line(app, n, old, top, self.replaceGrille, self.doneReplace, 0 + multi, time)
                time2 = column(app, n, old, left, self.replaceGrille, self.doneReplace, 1 + multi, time)
                return max(time1, time2)
            case "multi":
                self.setGrilles()
                multiFuncs = "_".join(funcs[1:]).split("__")
                self.nbFunc = sum(map(self.getNbFunc, multiFuncs))
                self.setGrilles()
                i = 0
                time = 0
                for f in multiFuncs:
                    time2 = self.lunchFunc(app, f, True, i, time)
                    if time2 > time: time = time2
                    i += self.getNbFunc(f)
                return time
            case "time":
                return self.lunchFunc(app, "_".join(funcs[2:]), isMulti, multi, n)
            case _:
                print("Erreur inconnu : ", func)
                return 1000

    def getNbFunc(self, name):
        match name:
            case "line":
                return 1
            case "column":
                return 1
            case "crossP":
                return 2
            case _:
                names = name.split("_")
                if len(names) == 1: return 0
                return self.getNbFunc(names[0])

    def setFunc(self, func):
        self.func = func

    def setGrilles(self):
        self.grilles = [None for _ in range(0, self.nbFunc)]

    def replaceGrille(self, x, y, n, old, i):
        if self.grilles[i] is None:
            self.grilles[i] = copy.deepcopy(self.grille)
        if self.grilles[i][x][y] == old:
            self.grilles[i][x][y] = n

    def doneReplace(self):
        self.nbFuncDone += 1
        if self.nbFuncDone == self.nbFunc:
            # print("hi")
            for i in range(0, SIZE[0]):
                for j in range(0, SIZE[1]):
                    n = max([self.grilles[k][i][j] for k in range(0, self.nbFunc)])
                    self.grille[i][j] = n
                    self.func(i, j, n)
            self.nbFuncDone = 0

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
