import time
from variable import *
from Static import Static


def colAux(y, n, old, replaceGrille, nbFunc):
    for i in range(0, SIZE[1]):
        replaceGrille(i, y, n, old, nbFunc)


def colStarter(name, n, old, left, i, step, timer, replaceGrille, nbFunc):
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
    Static.event.add(colStarter, 1, n, old, left, i, step, timer, replaceGrille, nbFunc)
    return


def column(n, old, left, replaceGrille, nbFunc, wait=0):
    Static.event.add(colStarter, int(wait * 1000), n, old, left, 0 if left else SIZE[1] - 1, 1 if left else -1, None,
              replaceGrille, nbFunc)
    return DELAY * SIZE[1] + wait
