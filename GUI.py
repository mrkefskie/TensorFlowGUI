from tkinter import *
from tkinter.filedialog import askdirectory

from os import listdir

class GUI(Frame):
    """This class will handle all the input and output to the GUI"""
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.parent.title("TensorFlow GUI")

        self.parent.state('zoomed')

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)

        closebutton = Button(self, text="Exit program", command=self.exitButton)
        closebutton.pack(side=RIGHT, padx=5, pady=5)

    def exitButton(self):
        Frame.quit(self)
        self.quit()
