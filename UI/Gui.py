from variable import *
import pygame
import threading
from Static import Static
from UI.Element.RadioButton import RadioButton
from UI.Element.Button import Button

class Gui(threading.Thread):
    def __init__(self, startLevel, nbLevel, completeLevel):
        pygame.init()
        threading.Thread.__init__(self)
        self.completeLevel = completeLevel
        self.widthGrille = SIZE[0] * SIZEPLATE[0]
        self.heightGrille = SIZE[1] * SIZEPLATE[1]
        self.width = self.widthGrille + 350
        self.height = self.heightGrille
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.plates = []
        for _ in range(0, SIZE[0]):
            row = []
            for _ in range(0, SIZE[1]):
                row.append(0)
            self.plates.append(row)
        self.isRunning = False

        font = pygame.font.SysFont(None, 25)

        self.radioButtons = [
            RadioButton(self.widthGrille + 50, 40 * (i + 1), 100, 30, font, "Level " + str(i + 1))
            for i in range(0, nbLevel)
        ]
        for radioButtons in self.radioButtons:
            radioButtons.setRadioButtons(self.radioButtons)
        self.radioButtons[0].clicked = True

        buttonPlay = Button(self.widthGrille + 200, 40, 100, 30, font, "Play", lambda: self.startLevel(startLevel))
        buttonStop = Button(self.widthGrille + 200, 80, 100, 30, font, "Stop", self.stopLevel)
        buttonComplete = Button(self.widthGrille + 200, 120, 100, 30, font, "Complete", self.completeLevel)

        self.group = pygame.sprite.Group(self.radioButtons, buttonPlay, buttonStop, buttonComplete)
        Static.event.registerEvent(self.group.update)

    def startLevel(self, func):
        level = "1"
        for radio in self.radioButtons:
            if radio.clicked:
                level = radio.text[6:]
                break
        func(level)

    def stopLevel(self):
        Static.event.stopAll()

    def completeLevel(self):
        self.completeLevel()
        self.stopLevel()

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
                pygame.draw.rect(self.screen, COLOR[self.plates[i][j]],
                                 (i * SIZEPLATE[0], j * SIZEPLATE[1], SIZEPLATE[0], SIZEPLATE[1]))

    def start(self):
        self.isRunning = True
        self.loop()

    def stop(self):
        self.isRunning = False

    def loop(self):
        while self.isRunning:
            self.clock.tick(FPS)
            self.screen.fill((0, 0, 0))
            Static.event.inEvent()
            self.group.draw(self.screen)
            self.draw()
            pygame.display.flip()
