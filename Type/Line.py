import time
from variable import *

import customtkinter


def lineAux(x, n, old, replaceGrille, nbGrille):
    for i in range(0, SIZE[0]):
        replaceGrille(x, i, n, old, nbGrille)


def lineStarter(app: customtkinter.CTkBaseClass, n, old, top, i, step, timer, replaceGrille, nbGrille):
    if (time.time() - timer) >= (DELAY * (i if top else (SIZE[0] - 1 - i))):
        if i != (SIZE[0] if top else -1):
            if i != (0 if top else SIZE[0] - 1):
                lineAux(i - step, old, n, replaceGrille, nbGrille)
            lineAux(i, n, old, replaceGrille, nbGrille)
        i += step
    if i == (SIZE[0] + 1 if top else -2):
        lineAux(SIZE[0] - 1 if top else 0, old, n, replaceGrille, nbGrille)
        return
    app.after(1, lineStarter, app, n, old, top, i, step, timer, replaceGrille, nbGrille)
    return DELAY * SIZE[0]


def line(app: customtkinter.CTkBaseClass, n, old, top, replaceGrille):
    return lineStarter(app, n, old, top, 0 if top else SIZE[0] - 1, 1 if top else -1, time.time(), replaceGrille,
                       0)
