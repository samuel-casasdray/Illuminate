import time
from variable import *
from Static import Static

def diagonalAux(x0, x1, y0, y1, n, old, replaceGrille, nbFunc):
    stepX = 1 if x1 > x0 else -1
    stepY = 1 if y1 > y0 else -1
    for i in range(0, abs(x0 - (x1 + stepX))):
        replaceGrille(x0 + stepX * i, y0 + stepY * i, n, old, nbFunc)


def diagonalStarter(name, n, old, x0, x1, x2, x3, y0, y1, y2, y3, top, left, i, timer, replaceGrille, nbFunc):
    if timer is None: timer = time.time()
    done = False
    if (time.time() - timer) >= DELAY * i:
        if i < SIZE[0] + SIZE[1]:
            if i != 1:
                diagonalAux(x2, x3, y2, y3, old, n, replaceGrille, nbFunc)
            diagonalAux(x0, x1, y0, y1, n, old, replaceGrille, nbFunc)
        done = True
        i += 1
    if done:
        if x0 == x1 and y0 == y1 and i == SIZE[0] + SIZE[1] + 1:
            diagonalAux(x0, x0, y0, y0, old, n, replaceGrille, nbFunc)
            return
        x2 = x0
        x3 = x1
        y2 = y0
        y3 = y1
        if i != SIZE[0] + SIZE[1]:
            if (left and x0 == 0) or (not left and x0 == SIZE[0] - 1):
                y0 += (1 if top else -1)
                x1 += (-1 if left else 1)
            else:
                y1 += (1 if top else -1)
                x0 += (-1 if left else 1)
    Static.event.add(diagonalStarter, 1, n, old, x0, x1, x2, x3, y0, y1, y2, y3, top, left, i, timer, replaceGrille, nbFunc)


def diagonal(n, old, top, left, replaceGrille, nbFunc, wait=0):
    x0 = SIZE[0] - 1 if left else 0
    y0 = 0 if top else SIZE[1] - 1
    Static.event.add(diagonalStarter, wait * 1000, n, old, x0, x0, None, None, y0, y0, None, None, top, left, 1, None, 
                     replaceGrille, nbFunc)
    return DELAY * (SIZE[0] + SIZE[1] - 1) + wait