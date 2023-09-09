import time
from variable import *
import customtkinter


def colAux(y, n, old, replaceGrille, nbFunc):
    for i in range(0, SIZE[1]):
        replaceGrille(i, y, n, old, nbFunc)


def colStarter(app: customtkinter.CTkBaseClass, n, old, left, i, step, timer, replaceGrille, done, nbFunc):
    if (time.time() - timer) >= (DELAY * (i if left else (SIZE[1] - 1 - i))):
        if i != (SIZE[1] if left else -1):
            if i != (0 if left else SIZE[1] - 1):
                colAux(i - step, old, n, replaceGrille, nbFunc)
            colAux(i, n, old, replaceGrille, nbFunc)
            if (i + step) != (SIZE[1] + 1 if left else -2):
                done()
        i += step
    if i == (SIZE[1] + 1 if left else -2):
        colAux(SIZE[1] - 1 if left else 0, old, n, replaceGrille, nbFunc)
        done()
        return
    app.after(1, colStarter, app, n, old, left, i, step, timer, replaceGrille, done, nbFunc)
    return


def column(app: customtkinter.CTkBaseClass, n, old, left, replaceGrille, done, nbFunc, wait=0):
    app.after(int(wait * 1000), colStarter, app, n, old, left, 0 if left else SIZE[1] - 1, 1 if left else -1, time.time(),
              replaceGrille, done, nbFunc)
    return DELAY * SIZE[1]
