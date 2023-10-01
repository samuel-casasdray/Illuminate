import time
from variable import *
from Static import Static
import random as rd

pattern = [8, 9, 8, 9]

def randomAux(name, coords, n, old, i, replaceGrille, nbFunc):
    for coord in coords:
        replaceGrille(coord[0], coord[1], pattern[i] if i < len(pattern) else n, old if i == 0 else pattern[i - 1], nbFunc)
    if i == len(pattern):
        return
    Static.event.add(randomAux, DELAY * 300, coords, n, old, i + 1, replaceGrille, nbFunc)


def randomStarter(name, n, old, array, i, timer, replaceGrille, nbFunc):
    if timer is None: timer = time.time()
    if (time.time() - timer) >= (DELAY * 2) * i:
        if i < len(array):
            Static.event.add(randomAux, DELAY * 300, array[i], n, old, 0, replaceGrille, nbFunc)
        i+=1
    if i == len(array) + 1:
        for j in range(SIZE[0]):
            for k in range(SIZE[1]):
                replaceGrille(j, k, old, n, nbFunc)
        return
    Static.event.add(randomStarter, 1, n, old, array, i, timer, replaceGrille, nbFunc)


def random(n, old, replaceGrille, nbFunc, wait=0):
    randomArray = fill([])
    Static.event.add(randomStarter, wait * 1000, n, old, randomArray, 0, None, replaceGrille, nbFunc)
    return DELAY * (len(randomArray)) * 2 + wait

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
    while nb != SIZE[0] * SIZE[1]:
        step = []
        for _ in range(rd.choices(range(1, 10), [0.07, 0.09, 0.12, 0.14, 0.16, 0.14, 0.12, 0.09, 0.07])[0]):
            i = rd.randint(0, SIZE[0] - 1)
            j = rd.randint(0, SIZE[1] - 1)
            while isIn(array, [i, j]) or isIn([step], [i, j]):
                i = rd.randint(0, SIZE[0] - 1)
                j = rd.randint(0, SIZE[1] - 1)
            step.append([i, j])
            nb += 1
            if nb == SIZE[0] * SIZE[1]: break
        array.append(step)
    return array
            
