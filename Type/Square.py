import time
from variable import *
import customtkinter


def squareStarter(app: customtkinter.CTkBaseClass, n, old, x, y, i, timer, replaceGrille, nbFunc):
    if (time.time() - timer) >= (DELAY * i):
        for j in range(x - i, x + 1 + i):
            replaceGrille(j, y, n, old, nbFunc)
            replaceGrille(j, y, n, old, nbFunc)
        for j in range(y - i, y + 1 + i):
            replaceGrille(x, j, n, old, nbFunc)
            replaceGrille(x, j, n, old, nbFunc)
        i += 1
    app.after(1, squareStarter, app, n, old, x, y, i, timer, replaceGrille, nbFunc)
    return


def square(app: customtkinter.CTkBaseClass, n, old, x, y, replaceGrille, nbFunc, wait=0):
    app.after(int(wait * 1000), squareStarter, app, n, old, x, y, 0, time.time(), replaceGrille, nbFunc)
    return max(x, y, SIZE[0] - x, SIZE[1] - y) * DELAY + wait
