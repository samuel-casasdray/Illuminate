import time
from variable import *
import customtkinter


def colAux(y, n, old, replaceGrille, nbGrille):
    for i in range(0, SIZE[1]):
        replaceGrille(i, y, n, old, nbGrille)


def colStarter(app: customtkinter.CTkBaseClass, n, old, left, i, step, timer, replaceGrille, nbGrille):
    if (time.time() - timer) >= (DELAY * (i if left else (SIZE[1] - 1 - i))):
        if i != (SIZE[1] if left else -1):
            if i != (0 if left else SIZE[1] - 1):
                colAux(i - step, old, n, replaceGrille, nbGrille)
            colAux(i, n, old, replaceGrille, nbGrille)
        i += step
    if i == (SIZE[1] + 1 if left else -2):
        colAux(SIZE[1] - 1 if left else 0, old, n, replaceGrille, nbGrille)
        return
    app.after(1, colStarter, app, n, old, left, i, step, timer, replaceGrille, nbGrille)
    return DELAY * SIZE[1]


def column(app: customtkinter.CTkBaseClass, n, old, left, replaceGrille):
    return colStarter(app, n, old, left, 0 if left else SIZE[1] - 1, 1 if left else -1, time.time(), replaceGrille,
                      0)
