from game import *
from variable import *

color = {0: "#000", 1: "#d62828", 2: "#fee440", 3: "#7ae582", 4: "#0077b6"}


class Grille(customtkinter.CTkFrame):
    def __init__(self, master, sizePlateX, sizePlateY, **kwargs):
        super().__init__(master, **kwargs)
        self.width = SIZE[0] * sizePlateX
        self.height = SIZE[1] * sizePlateY
        self.configure(width=self.width, height=self.height)
        for i in range(0, SIZE[0]):
            self.grid_rowconfigure(i, weight=1)
        for i in range(0, SIZE[1]):
            self.grid_columnconfigure(i, weight=1)
        self.plates = []
        for i in range(0, SIZE[0]):
            row = []
            for j in range(0, SIZE[1]):
                frame = Plate(master=self, fg_color=color[0])
                frame.configure(height=sizePlateY, width=sizePlateX)
                row.append(frame)
                frame.grid(row=i, column=j)
            self.plates.append(row)

    def changeColor(self, x, y, i):
        self.plates[x][y].configure(fg_color=color[i])

    def getSize(self):
        return str(self.width) + "x" + str(self.height)

    def loadGrille(self, grille):
        for i in range(0, SIZE[0]):
            for j in range(0, SIZE[1]):
                self.changeColor(i, j, grille[i][j])


class Plate(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.game.loadLevel('1')
        self.grille = Grille(master=self, sizePlateX=30, sizePlateY=30)
        self.geometry(self.grille.getSize())
        self.title("Illuminate")
        self.grille.grid(row=0, column=0)
        self.grille.loadGrille(self.game.grille)
        self.game.setFunc(self.grille.changeColor)
        self.after(2000, self.game.startGame, self)


app = App()
app.mainloop()
