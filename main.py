from game import *
from variable import *
import guizero

color = {0: "#000000", 1: "#d62828", 2: "#fee440", 3: "#7ae582", 4: "#0077b6"}

class GrilleZ(guizero.Box):
    def __init__(self, master, **kwargs):
        self._width = SIZE[0] * SIZEPLATE[0]
        self._height = SIZE[1] * SIZEPLATE[1]
        super().__init__(master=master, width=self._width, height=self._height, layout="grid", **kwargs)
        self.plates = []
        for i in range(0, SIZE[0]):
            row = []
            for j in range(0, SIZE[1]):
                row.append(Plate(master=self, grid=[i, j]))
            self.plates.append(row)

    def changeColor(self, x, y, i):
        self.plates[x][y].changeColor(i)

    def loadGrille(self, grille):
        for i in range(0, SIZE[0]):
            for j in range(0, SIZE[1]):
                self.changeColor(i, j, grille[i][j])


class Plate(guizero.Box):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, width=SIZEPLATE[0], height=SIZEPLATE[1], **kwargs)
        self.bg = color[0]

    def changeColor(self, i):
        self.bg = color[i]
        

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
                frame = customtkinter.CTkLabel(master=self, bg_color=color[0], text="")
                frame.configure(height=sizePlateY, width=sizePlateX)
                row.append(frame)
                frame.grid(row=i, column=j)
            self.plates.append(row)

    def changeColor(self, x, y, i):
        print(x, y, i)
        self.plates[x][y].configure(bg_color=color[i])

    def getSize(self):
        return str(self.width) + "x" + str(self.height)

    def loadGrille(self, grille):
        for i in range(0, SIZE[0]):
            for j in range(0, SIZE[1]):
                self.changeColor(i, j, grille[i][j])


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.game = Game()
        self.game.loadLevel('1')
        # self.grille = Grille(master=self, sizePlateX=30, sizePlateY=30)
        self.grille = GrilleZ(sizePlateX=30, sizePlateY=30)
        # self.geometry(self.grille.getSize())
        # self.resizable(False, False)
        # self.title("Illuminate")
        # self.grille.grid(row=0, column=0)
        # self.grille.loadGrille(self.game.grille)
        # self.game.setFunc(self.grille.changeColor)
        # self.after(0, self.game.startGame, self)

class AppZ(guizero.App):
    def __init__(self):
        self._width = SIZE[0] * SIZEPLATE[0]
        self._height = SIZE[1] * SIZEPLATE[1]
        super().__init__(title="Illuminate", width=self._width, height=self._height, layout="grid")
        self.game = Game()
        self.game.loadLevel('1')
        self.grille = GrilleZ(master=self, grid=[0,0])
        self.grille.loadGrille(self.game.grille)
        self.game.setFunc(self.grille.changeColor)
        self.after(0, self.game.startGame, args=[self])
        self.display()
        


# app = App()
# app.mainloop()
app = AppZ()