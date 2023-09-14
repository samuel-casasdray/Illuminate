from Game import Game
from variable import *
from Gui import Gui
from Static import Static

class App():
    def __init__(self):
        self.gui = Gui()
        self.game = Game(self.gui)
        self.startLevel('1')
        self.gui.run()

    def startLevel(self, level: str):
        self.game.loadLevel(level)
        self.gui.loadGrille(self.game.grille)
        Static.event.add(self.game.startGame, 1)


app = App()