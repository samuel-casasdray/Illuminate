from variable import *
import pygame
import threading
from Static import Static

class Gui(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.width = SIZE[0] * SIZEPLATE[0]
        self.height = SIZE[1] * SIZEPLATE[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.plates = []
        for _ in range(0, SIZE[0]):
            row = []
            for _ in range(0, SIZE[1]):
                row.append(0)
            self.plates.append(row)
        self.isRuning = False
    
    def run(self):
        self.start()

    def changeColor(self, x, y, i):
        self.plates[x][y] = i

    def loadGrille(self, grille):
        for i in range(0, SIZE[0]):
            for j in range(0, SIZE[1]):
                self.changeColor(i, j, grille[i][j])
        
    def draw(self):
        for i in range(0, SIZE[0]):
            for j in range(0, SIZE[1]):
                pygame.draw.rect(self.screen, COLOR[self.plates[i][j]], (i * SIZEPLATE[0], j * SIZEPLATE[1], SIZEPLATE[0], SIZEPLATE[1]))

    def start(self):
        self.isRuning = True
        self.loop()
    
    def stop(self):
        self.isRuning = False

    def loop(self):
        while self.isRuning:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            Static.event.inEvent()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()