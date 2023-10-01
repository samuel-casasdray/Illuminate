import time
from variable import *
from Static import Static
import random as rd

pattern = [8, 9, 8, 9]

def spreadAux(name, coords, n, old, i, replaceGrille, nbFunc):
    for coord in coords:
        replaceGrille(coord[0], coord[1], pattern[i] if i < len(pattern) else n, old if i == 0 else pattern[i - 1], nbFunc)
    if i == len(pattern):
        return
    Static.event.add(spreadAux, DELAY * 300, coords, n, old, i + 1, replaceGrille, nbFunc)


def spreadStarter(name, n, old, array, i, timer, replaceGrille, nbFunc):
    if timer is None: timer = time.time()
    if (time.time() - timer) >= (DELAY * 2) * i:
        if i < len(array):
            Static.event.add(spreadAux, DELAY * 300, array[i], n, old, 0, replaceGrille, nbFunc)
        i+=1
    if i == len(array) + 1:
        for j in range(SIZE[0]):
            for k in range(SIZE[1]):
                replaceGrille(j, k, old, n, nbFunc)
        return
    Static.event.add(spreadStarter, 1, n, old, array, i, timer, replaceGrille, nbFunc)


def spread(n, old, replaceGrille, nbFunc, wait=0):
    spreadArray = fill([])
    Static.event.add(spreadStarter, wait * 1000, n, old, spreadArray, 0, None, replaceGrille, nbFunc)
    return DELAY * (len(spreadArray)) * 2 + wait

def isIn(array: list, coord: list):
    for step in array:
        for coords in step:
            if coords[0] == coord[0] and coords[1] == coord[1]: 
                return True
    return False

def full(array: list):
    nb = 0
    for step in array:
        nb += len(step)
    return nb == SIZE[0] * SIZE[1]

def fill(array: list = []):
    nb = 0
    step = []
    for _ in range(rd.randint(3, 5)):
        i = rd.randint(0, SIZE[0] - 1)
        j = rd.randint(0, SIZE[1] - 1)
        while isIn([step], [i, j]):
            i = rd.randint(0, SIZE[0] - 1)
            j = rd.randint(0, SIZE[1] - 1)
        step.append([i, j])
        nb += 1
    array.append(step)
    while nb != SIZE[0] * SIZE[1]:
        step = []
        for coords in array[-1]:
            x = coords[0]
            y = coords[1]
            x0 = x + 1
            x1 = x - 1
            y0 = y + 1
            y1 = y - 1
            if 0 <= x0 <= SIZE[0] - 1 and not isIn(array, [x0, y]) and not isIn([step], [x0, y]):
                step.append([x0, y])
                nb += 1
            if 0 <= x1 <= SIZE[0] - 1 and not isIn(array, [x1, y]) and not isIn([step], [x1, y]):
                step.append([x1, y])
                nb += 1
            if 0 <= y0 <= SIZE[1] - 1 and not isIn(array, [x, y0]) and not isIn([step], [x, y0]):
                step.append([x, y0])
                nb += 1
            if 0 <= y1 <= SIZE[1] - 1 and not isIn(array, [x, y1]) and not isIn([step], [x, y1]):
                step.append([x, y1])
                nb += 1
            if nb == SIZE[0] * SIZE[1]: break
        array.append(step)
    return array
            
