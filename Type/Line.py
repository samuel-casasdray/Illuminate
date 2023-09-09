import time
from variable import *

import customtkinter


def lineAux(x, n, old, replaceGrille, nbFunc):
    for i in range(0, SIZE[0]):
        replaceGrille(x, i, n, old, nbFunc)


def lineStarter(app: customtkinter.CTkBaseClass, n, old, top, i, step, timer, replaceGrille, done, nbFunc):
    if (time.time() - timer) >= (DELAY * (i if top else (SIZE[0] - 1 - i))):
        if i != (SIZE[0] if top else -1):
            if i != (0 if top else SIZE[0] - 1):
                lineAux(i - step, old, n, replaceGrille, nbFunc)
            lineAux(i, n, old, replaceGrille, nbFunc)
            if (i + step) != (SIZE[0] + 1 if top else -2):
                done()
        i += step
    if i == (SIZE[0] + 1 if top else -2):
        lineAux(SIZE[0] - 1 if top else 0, old, n, replaceGrille, nbFunc)
        done()
        return
    app.after(1, lineStarter, app, n, old, top, i, step, timer, replaceGrille, done, nbFunc)
    return


def line(app: customtkinter.CTkBaseClass, n, old, top, replaceGrille, done, nbFunc, wait=0):
    app.after(int(wait * 1000), lineStarter, app, n, old, top, 0 if top else SIZE[0] - 1, 1 if top else -1, time.time(),
              replaceGrille, done, nbFunc)
    return DELAY * SIZE[0]
