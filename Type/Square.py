import time
from variable import *
import customtkinter


def colAux(y, n, old, replaceGrille):
    for i in range(0, SIZE[1]):
        replaceGrille(i, y, n, old)


def colStarter(app: customtkinter.CTkBaseClass, n, old, left, i, step, timer, replaceGrille):
    if (time.time() - timer) >= (DELAY * (i if left else (SIZE[1] - 1 - i))):
        if i != (SIZE[1] if left else -1):
            if i != (0 if left else SIZE[1] - 1):
                colAux(i - step, old, n, replaceGrille)
            colAux(i, n, old, replaceGrille)
        i += step
    if i == (SIZE[1] + 1 if left else -2):
        colAux(SIZE[1] - 1 if left else 0, old, n, replaceGrille)
        return
    app.after(1, colStarter, app, n, old, left, i, step, timer, replaceGrille)
    return DELAY * SIZE[1]


def column(app: customtkinter.CTkBaseClass, n, old, left, replaceGrille):
    return colStarter(app, n, old, left, 0 if left else SIZE[1] - 1, 1 if left else -1, time.time(), replaceGrille)
