import time
from variable import *
from Static import Static
import math

def circleStarter(name, n, old, x, y, i, timer, replaceGrille, nbFunc):
    if timer is None: timer = time.time()
    on = False
    if (time.time() - timer) >= (DELAY * i):
        if i == 0:
            replaceGrille(x, y, n, old, nbFunc)
            on = True
        else:
            if i == 1:
                replaceGrille(x, y, old, n, nbFunc)
            else:
                list_point = []
                for d in range(360):
                    list_point.append((round((i - 1)*math.cos(d)), round((i-1)*math.sin(d))))
                list_point = list(set([i for i in list_point]))
                for point in list_point:
                    if 0 <= x + point[0] < SIZE[0] and 0 <= y + point[1] < SIZE[1]:
                        replaceGrille(x + point[0], y + point[1], old, n, nbFunc)
            list_point = []
            for d in range(360):
                list_point.append((round(i*math.cos(d)), round(i*math.sin(d))))
            list_point = list(set([i for i in list_point]))
            for point in list_point:
                if 0 <= x + point[0] < SIZE[0] and 0 <= y + point[1] < SIZE[1]:
                    replaceGrille(x + point[0], y + point[1], n, old, nbFunc)
                    on = True
        i+=1
    else:
        on = True
    if not on: return
    Static.event.add(circleStarter, 1, n, old, x, y, i, timer, replaceGrille, nbFunc)


def circle(n, old, x, y, replaceGrille, nbFunc, wait=0):
    Static.event.add(circleStarter, wait * 1000, n, old, x, y, 0, None, replaceGrille, nbFunc)
    on = True
    i = -1
    while on:
        i += 1
        on = False
        list_point = []
        for d in range(360):
            list_point.append((round(i*math.cos(d)), round(i*math.sin(d))))
        list_point = list(set([i for i in list_point]))
        for point in list_point:
            if 0 <= x + point[0] < SIZE[0] and 0 <= y + point[1] < SIZE[1]:
                on = True
                break
    return (i + 1) * DELAY + wait

def pixel(x, y, p, q):
    return [(x+p, y+q), (x+p, y-q), (x-p, y+q), (x-p, y-q), (x+q, y+p), (x+q, y-p), (x-q, y+p), (x-q, y-p)]
