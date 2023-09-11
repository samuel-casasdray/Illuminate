import time
from variable import *
import customtkinter


def squareStarter(app: customtkinter.CTkBaseClass, n, old, x, y, i, timer, replaceGrille, nbFunc):
    if timer is None: timer = time.time()
    if (time.time() - timer) >= (DELAY * i):
        if i == 0:
            replaceGrille(x, y, n, old, nbFunc)
        else:
            for j in range(x - i, x + 1 + i):
                if 0 <= j < SIZE[0]:
                    if 0 <= y - i + 1 < SIZE[1]:
                        replaceGrille(j, y - i + 1, old, n, nbFunc)
                    if 0 <= y + i - 1 < SIZE[1]:
                        replaceGrille(j, y + i - 1, old, n, nbFunc)
            for j in range(y - i, y + 1 + i):
                if 0 <= j < SIZE[1]:
                    if 0 <= x - i + 1 < SIZE[0]:
                        replaceGrille(x - i + 1, j, old, n, nbFunc)
                    if 0 <= x + i - 1 < SIZE[0]:
                        replaceGrille(x + i - 1, j, old, n, nbFunc)
            for j in range(x - i, x + 1 + i):
                if 0 <= j < SIZE[0]:
                    if 0 <= y - i < SIZE[1]:
                        replaceGrille(j, y - i, n, old, nbFunc)
                    if 0 <= y + i < SIZE[1]:
                        replaceGrille(j, y + i, n, old, nbFunc)
            for j in range(y - i, y + 1 + i):
                if 0 <= j < SIZE[1]:
                    if 0 <= x - i < SIZE[0]:
                        replaceGrille(x - i, j, n, old, nbFunc)
                    if 0 <= x + i < SIZE[0]:
                        replaceGrille(x + i, j, n, old, nbFunc)
        i += 1
    app.after(1, squareStarter, app, n, old, x, y, i, timer, replaceGrille, nbFunc)
    return


def square(app: customtkinter.CTkBaseClass, n, old, x, y, replaceGrille, nbFunc, wait=0):
    app.after(int(wait * 1000), squareStarter, app, n, old, x, y, 0, None, replaceGrille, nbFunc)
    return max(x, y, SIZE[0] - x, SIZE[1] - y) * DELAY + wait
