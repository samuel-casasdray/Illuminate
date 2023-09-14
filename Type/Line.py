import time
from variable import *
from Static import Static


def lineAux(x, n, old, replaceGrille, nbFunc):
    for i in range(0, SIZE[0]):
        replaceGrille(x, i, n, old, nbFunc)


def lineStarter(name, n, old, top, i, step, timer, replaceGrille, nbFunc):
    if timer is None: timer = time.time()
    if (time.time() - timer) >= DELAY * (i if top else (SIZE[0] - 1 - i)):
        if i != (SIZE[0] if top else -1):
            if i != (0 if top else SIZE[0] - 1):
                lineAux(i - step, old, n, replaceGrille, nbFunc)
            lineAux(i, n, old, replaceGrille, nbFunc)
        i += step
    Static.event.stop(name)
    if i == (SIZE[0] + 1 if top else -2):
        lineAux(SIZE[0] - 1 if top else 0, old, n, replaceGrille, nbFunc)
        return
    Static.event.add(lineStarter, 1, n, old, top, i, step, timer, replaceGrille, nbFunc)


def line(n, old, top, replaceGrille, nbFunc, wait=0):
    Static.event.add(lineStarter, wait * 1000, n, old, top, 0 if top else SIZE[0] - 1, 1 if top else -1, None,
              replaceGrille, nbFunc)
    return DELAY * SIZE[0] + wait
