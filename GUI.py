from tkinter import *
from tkinter.filedialog import askdirectory

from tkinter import messagebox


from os import listdir


class GUI(Frame):
    """This class will handle all the input and output to the GUI"""

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent

        self.label_amount = ""

        self.working_directory = ""
        self.file_list = []

        self.initUI()

    def initUI(self):
        self.parent.title("TensorFlow GUI")

        self.parent.state('zoomed')

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)

        # EXIT BUTTON
        closebutton = Button(self, text="Exit program", command=self.exitButton)
        closebutton.pack(side=RIGHT, padx=5, pady=5)

        # FOLDER SELECT BUTTON
        folderselectbutton = Button(self, text="Select folder", command=self.folderSelecter)
        folderselectbutton.pack(side=RIGHT)

        # AMOUNT TO PROCESS LABEL
        self.label_amount = Label(self, text="", background="white")
        self.label_amount.pack(side=LEFT)

    def exitButton(self):
        Frame.quit(self)
        self.quit()

    def folderSelecter(self):
        self.working_directory = askdirectory(parent=self.parent,
                                              initialdir=r"E:\testCaseSelector\30-01-2017 18-20\Color",
                                              title='Choose working directory')
        print(self.working_directory)

        fileListRaw = [f for f in listdir(self.working_directory) if (f.endswith(".jpg") & f[0].isdigit())]

        if len(fileListRaw) > 0:  # Check if there are files in the directory
            current_file = 0  # Set the current file to the first one
        else:
            # Display an error
            messagebox.showerror("Error", "Directory is empty")
            self.label_amount['text'] = "NO FILES FOUND"
            self.label_amount['foreground'] = "red"
            return

        last_file = current_file
        found_files = []

        # Let's look for output that is already there, and remove all fields from the list we already got
        try:
            with open(self.working_directory + '/' + 'output.txt', 'r') as f:
                lines = f.readlines()
                for line in lines:
                    FF = line.split(',', 1)[0]
                    found_files.append(str(FF) + '.jpg')

                # We should have a list of already processed files, we throw out all of that
                self.file_list = [x for x in fileListRaw if x not in found_files]
        except FileNotFoundError:
            self.file_list = fileListRaw
            print("No previous output file found")

        self.label_amount['foreground'] = "black"
        self.label_amount['text'] = "{} JPG's in folder, {} already processed, {} left to process.".format(
            len(fileListRaw), len(found_files), len(self.file_list))
