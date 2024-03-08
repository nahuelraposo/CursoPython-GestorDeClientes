from tkinter import *

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor de clientes")

    def build(self):
        self.button = Button(self, text="Hola", command=self.hola)
        self.button.pack()

    def hola(self):
        print("Hola mundo")

if __name__ == "__main__":
    app = MainWindow()
    app.build()
    app.mainloop()