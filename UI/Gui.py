from variable import *
import pygame
import threading
from Static import Static
from UI.Element.RadioButton import RadioButton
from UI.Element.Button import Button


class Gui(threading.Thread):
    def __init__(self, startLevel, nbLevel, completeLevelFunc):
        pygame.init()
        threading.Thread.__init__(self)
        self.completeLevelFunc = completeLevelFunc
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
        self.isComplete = False

        self.font = pygame.font.SysFont("comicsansms", 20)

        self.radioButtons = [
            RadioButton(self.widthGrille + 50, 40 * (i + 1), 100, 30, self.font, "Level " + str(i + 1))
            for i in range(0, nbLevel)
        ]
        for radioButtons in self.radioButtons:
            radioButtons.setRadioButtons(self.radioButtons)
        self.radioButtons[0].clicked = True

        buttonPlay = Button(self.widthGrille + 200, 40, 100, 30, self.font, "Play", lambda: self.startLevel(startLevel))
        buttonStop = Button(self.widthGrille + 200, 80, 100, 30, self.font, "Stop", self.stopLevel)
        buttonComplete = Button(self.widthGrille + 200, 120, 100, 30, self.font, "Complete", self.completeLevel)

        self.group = pygame.sprite.Group(self.radioButtons, buttonPlay, buttonStop, buttonComplete)
        Static.event.registerEvent(self.group.update)
        self.start_time = None
        self.time_hms = 0, 0, 0, 0
        self.timer_surf = self.font.render(self.renderTimer(), True, (255, 255, 255))

    def startLevel(self, func):
        level = "1"
        for radio in self.radioButtons:
            if radio.clicked:
                level = radio.text[6:]
                break
        self.start_time = pygame.time.get_ticks()
        self.isComplete = False
        func(level)

    def stopLevel(self):
        Static.event.stopAll()
        self.isComplete = True

    def completeLevel(self):
        self.completeLevelFunc()
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
            time_ms = (pygame.time.get_ticks() - self.start_time) if self.start_time is not None else 0
            new_hms = (time_ms // (1000 * 60 * 60)) % 24, (time_ms // (1000 * 60)) % 60, (time_ms // 1000) % 60, (
                time_ms) % 1000
            if new_hms != self.time_hms and not self.isComplete:
                self.time_hms = new_hms
                self.timer_surf = self.font.render(self.renderTimer(), True, (255, 255, 255))
            self.screen.blit(self.timer_surf, (self.widthGrille + 50, 10))
            pygame.display.flip()

    def renderTimer(self):
        return f'{self.time_hms[0]:02d}:{self.time_hms[1]:02d}:{self.time_hms[2]:02d}:{self.time_hms[3]:03d}'
