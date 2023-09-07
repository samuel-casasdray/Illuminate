import json
import customtkinter
from variable import *
from Type.Line import line
from Type.Column import column
from Type.CrossP import crossP


class Game:
    def __init__(self):
        self.stepLevel = 0
        self.func = None
        self.maxStep = 0
        self.level = None
        self.grille = []
        self.grilles = []
        self.nbFunc = 0
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
        self.step = 0

    def stopGame(self):
        self.levelInGoing = False

    def startGame(self, app: customtkinter.CTkBaseClass):
        self.levelInGoing = True
        self.loop(app)

    def loop(self, app: customtkinter.CTkBaseClass):
        self.stepLevel += 1
        if self.stepLevel > self.maxStep:
            self.stepLevel = 1
        error = self.level["error"][str(self.stepLevel)].split("_")
        func = error[0]
        n = int(error[1])
        old = int(error[2])
        match func:
            case "line":
                top = error[3] == "true"
                self.nbFunc = 1
                self.setGrilles()
                time = line(app, n, old, top, self.replaceGrille)
            case "col":
                left = error[3] == "true"
                self.nbFunc = 1
                self.setGrilles()
                time = column(app, n, old, left, self.replaceGrille)
            case "crossP":
                top = error[3] == "true"
                left = error[4] == "true"
                self.nbFunc = 2
                self.setGrilles()
                time = crossP(app, n, old, top, left, self.replaceGrille)
            case _:
                time = 1000
                print("Erreur inconnu : ", error)
        app.after(int(time * 1000), self.loop, app)

    def setFunc(self, func):
        self.func = func

    def setGrilles(self):
        self.grilles = [None for i in range(0, self.nbFunc)]

    def replaceGrille(self, x, y, n, old, i):
        if self.grille[x][y] == old:
            self.grille[x][y] = n
            self.func(x, y, n)

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
