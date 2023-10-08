import time
from variable import *
from Static import Static

def bounceStarter(name, n, old, x0, y0, size, stepX, stepY, bounce, i, timer, replaceGrille, nbFunc):
    if timer is None: timer = time.time()
    if (time.time() - timer) >= (DELAY * i):
        replaceGrille(x0 - stepX, y0 - stepY, old, n, nbFunc)
        replaced = False
        for j in range(min(i, size)):
            x = x0 + j * stepX
            y = y0 + j * stepY
            if x < 0 and bounce > 0:
                x = -x
            elif x > SIZE[0] - 1 and bounce > 0:
                x = (SIZE[0] - 1) - abs(SIZE[0] - 1 - x)
            if y < 0 and bounce > 0:
                y = -y
            elif y > SIZE[1] - 1 and bounce > 0:
                y = (SIZE[1] - 1) - abs(SIZE[1] - 1 - y)
            if not (0 > x or x > SIZE[0] - 1 or 0 > y or y > SIZE[1] - 1) and bounce >= 0:
                replaceGrille(x, y, n, old, nbFunc)
                print(x, y)
                replaced = True
        print(bounce)
        if not replaced and bounce == -1:
            return
        if bounce >= 0 and i > size:
            x0 += stepX
            y0 += stepY
            if x0 < 0:
                x0 = -x0
                stepX = 1
                bounce -= 1
            elif x0 > SIZE[0] - 1:
                x0 = (SIZE[0] - 1) - abs(SIZE[0] - 1 - x0)
                stepX = -1
                bounce -= 1
            if y0 < 0:
                y0 = -y0
                stepY = 1
                bounce -= 1
            elif y0 > SIZE[1] - 1:
                y0 = (SIZE[1] - 1) - abs(SIZE[1] - 1 - y0)
                stepY = -1
                bounce -= 1
        i += 1
    Static.event.add(bounceStarter, 1, n, old, x0, y0, size, stepX, stepY, bounce, i, timer, replaceGrille, nbFunc)


def bounce(n, old, x, y, size, angle, bounce, replaceGrille, nbFunc, wait=0):
    angle %= 8
    stepX = 1 if angle == 0 or angle == 1 or angle == 7 else (0 if angle == 2 or angle == 6 else -1)
    stepY = -1 if angle == 1 or angle == 2 or angle == 3 else (0 if angle == 0 or angle == 4 else 1)
    Static.event.add(bounceStarter, wait * 1000, n, old, x, y, size, stepX, stepY, bounce - 1, 0, None, replaceGrille, nbFunc)
    return 20
