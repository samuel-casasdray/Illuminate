import time
from variable import *
import customtkinter
import guizero


def colAux(y, n, old, replaceGrille, nbFunc):
    for i in range(0, SIZE[1]):
        replaceGrille(i, y, n, old, nbFunc)


def colStarter(app: guizero.App, n, old, left, i, step, timer, replaceGrille, nbFunc):
    if timer is None: timer = time.time()
    if (time.time() - timer) >= DELAY * (i if left else (SIZE[1] - 1 - i)):
        if i != (SIZE[1] if left else -1):
            if i != (0 if left else SIZE[1] - 1):
                colAux(i - step, old, n, replaceGrille, nbFunc)
            colAux(i, n, old, replaceGrille, nbFunc)
        i += step
    if i == (SIZE[1] + 1 if left else -2):
        colAux(SIZE[1] - 1 if left else 0, old, n, replaceGrille, nbFunc)
        return
    app.after(1, colStarter, [app, n, old, left, i, step, timer, replaceGrille, nbFunc])
    return


def column(app: guizero.App, n, old, left, replaceGrille, nbFunc, wait=0):
    app.after(int(wait * 1000), colStarter, app, n, old, left, 0 if left else SIZE[1] - 1, 1 if left else -1, None,
              replaceGrille, nbFunc)
    return DELAY * SIZE[1] + wait
