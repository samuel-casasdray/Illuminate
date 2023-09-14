import pygame

class Event:
    def __init__(self) -> None:
        self.events = [None for _ in range(0, 8)]
    
    def getName(self):
        return pygame.event.custom_type()

    def add(self, func, ms, *args):
        for i in range(0, 8):
            if self.events[i] is None:
                event = pygame.event.custom_type()
                pygame.time.set_timer(event, 1 if ms == 0 else int(ms))
                self.events[i] = (event, func, args)
                return True
        return False

    def stop(self, event):
        for i in range(0, 8):
            if self.events[i] is not None and self.events[i][0] == event:
                pygame.time.set_timer(event, 0)
                self.events[i] = None

    def inEvent(self):
        for i in range(0, 8):
            if self.events[i] is not None:
                if pygame.event.get(self.events[i][0]):
                    self.events[i][1](self.events[i][0], *self.events[i][2])

    