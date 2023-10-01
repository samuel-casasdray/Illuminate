from time import time
import pygame

class Event:
    def __init__(self) -> None:
        self.events = []
        self.registerEvents = []

    def registerEvent(self, func):
        self.registerEvents.append(func)

    def add(self, func, ms, *args):
        self.events.append((len(self.events), func, 1 if ms == 0 else ms, time(), args))
        return len(self.events) - 1

    def stop(self, event):
        del self.events[event]

    def stopAll(self):
        self.events = []

    def inEvent(self):
        indexs = []
        for i in range(len(self.events)):
            event = self.events[i]
            if (time() - event[3]) * 1000 >= event[2]:
                event[1](event[0], *event[4])
                indexs.append(i)
        indexs.sort(reverse=True)
        for i in indexs:
            del self.events[i]
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        for event in self.registerEvents:
            event(events)

    