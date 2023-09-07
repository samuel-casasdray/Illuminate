import time
from variable import *
import customtkinter
from Type.Column import colAux
from Type.Line import lineAux


def crossPStarter(app: customtkinter.CTkBaseClass, n, old, top, left, iTop, iLeft, stepTop, stepLeft, timer,
                  replaceGrille, nbGrille):
    needBreak = False
    didLine = False
    if (time.time() - timer) >= (DELAY * (iTop if top else (SIZE[0] - 1 - iTop))):
        if iTop != (SIZE[0] if top else -1):
            if iTop != (0 if top else SIZE[0] - 1):
                lineAux(iTop - stepTop, old, n, replaceGrille, nbGrille)
            lineAux(iTop, n, old, replaceGrille, nbGrille)
            didLine = True
        iTop += stepTop
    if iTop == (SIZE[0] + 1 if top else -2):
        lineAux(SIZE[0] - 1 if top else 0, old, n, replaceGrille, nbGrille)
        needBreak = True
    if (time.time() - timer) >= (DELAY * (iLeft if left else (SIZE[1] - 1 - iLeft))):
        if iLeft != (SIZE[1] if left else -1):
            if iLeft != (0 if left else SIZE[1] - 1):
                colAux(iLeft - stepLeft, old, n, replaceGrille, nbGrille)
            colAux(iLeft, n, old, replaceGrille, nbGrille)
            if didLine:
                replaceGrille(iTop - stepTop, iLeft - (0 if (iLeft == SIZE[1] - 1 and not left) else stepLeft), n, old, nbGrille)
        iLeft += stepLeft
    if iLeft == (SIZE[1] + 1 if left else -2):
        colAux(SIZE[1] - 1 if left else 0, old, n, replaceGrille, nbGrille)
        needBreak = True
    if needBreak: return
    app.after(1, crossPStarter, app, n, old, top, left, iTop, iLeft, stepTop, stepLeft, timer, replaceGrille, nbGrille)
    return DELAY * SIZE[1]


def crossP(app: customtkinter.CTkBaseClass, n, old, top, left, replaceGrille):
    return crossPStarter(app, n, old, top, left, 0 if top else SIZE[0] - 1, 0 if left else SIZE[1] - 1,
                         1 if top else -1, 1 if left else -1, time.time(), replaceGrille, 0)
