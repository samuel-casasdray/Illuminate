from Game import Game
from UI.Gui import Gui
from Static import Static


class App:
    def __init__(self):
        self.game = Game()
        self.gui = Gui(self.startLevel, self.game.countNbLevel(), self.game.completeLevel)
        self.game.setGui(self.gui)
        self.gui.run()

    def startLevel(self, level: str):
        self.game.loadLevel(level)
        self.gui.loadGrille(self.game.grille)
        Static.event.add(self.game.startGame, 1)


app = App()
