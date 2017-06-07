from tkinter import *
from tkinter.filedialog import askdirectory

from tkinter import messagebox

from os import listdir

from PIL import ImageTk

class GUI(Frame):
    """This class will handle all the input and output to the GUI"""

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent

        self.canvasW = 1280
        self.canvasH = 720

        self.current_file = 0

        self.label_amount = ""

        self.working_directory = ""
        self.file_list = []

        self.canvas = ""
        self.next_button = ""
        self.prev_button = ""

        self.image = ImageTk.PhotoImage(file='placeholder.jpg')
        self.imageW = self.image.width()
        self.imageH = self.image.height()

        self.scalar = self.imageW / self.canvasW

        self.initUI()

        self.startMouseX = 0
        self.startMouseY = 0

        self.tmpBoundingBox = ''

        self.boundingBoxCounter = 0
        self.boundingBox = []

        self.total_amount_of_images = 0
        self.amount_of_processed_images = 0
        self.amount_of_images_to_process = 0

    def initUI(self):
        self.parent.title("TensorFlow GUI")

        self.parent.state('zoomed')

        self.parent.bind("<BackSpace>", self.backspacePressed)
        self.parent.bind("<Right>", self.rightPressed)
        self.parent.bind("<Left>", self.leftPressed)

        # CANVAS FOR THE IMAGES
        self.canvas = Canvas(self, width=self.canvasW, height=self.canvasH)
        self.canvas.pack(fill=BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.canvasClick)
        self.canvas.bind("<B1-Motion>", self.canvasDrag)
        self.canvas.bind("<ButtonRelease-1>", self.canvasRelease)
        self.tmpBoundingBox = self.canvas.create_rectangle(0, 0, 0, 0)

        self.showImage('placeholder.jpg')

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)

        # EXIT BUTTON
        closebutton = Button(self, text="Exit program", command=self.exitButton)
        closebutton.pack(side=RIGHT, padx=5, pady=5)

        # FOLDER SELECT BUTTON
        folderselectbutton = Button(self, text="Select folder", command=self.folderSelecter)
        folderselectbutton.pack(side=RIGHT, padx=(100, 5))

        # NEXT BUTTON
        self.next_button = Button(self, text="Next", command=self.nextButton)
        self.next_button.pack(side=RIGHT, padx=5)
        self.next_button['state'] = 'disabled'

        # PREVIOUS BUTTON
        self.prev_button = Button(self, text="Previous", command=self.prevButton)
        self.prev_button.pack(side=RIGHT)
        self.prev_button['state'] = 'disabled'

        # AMOUNT TO PROCESS LABEL
        self.label_amount = Label(self, text="", background="white")
        self.label_amount.pack(side=LEFT)

    def backspacePressed(self, event):
        tmpboundingBoxes = self.boundingBox[:]

        self.canvas.delete(self.boundingBox[-1])

        del self.boundingBox[-1]
        self.boundingBoxCounter -= 1

    def rightPressed(self, event):
        self.showNextImage()

    def leftPressed(self, event):
        self.showPrevImage()

    def canvasClick(self, event):
        self.startMouseX = event.x
        self.startMouseY = event.y

    def canvasDrag(self, event):
        self.canvas.delete(self.tmpBoundingBox)
        self.tmpBoundingBox = event.widget.create_rectangle(self.startMouseX, self.startMouseY,
                                                            event.x, event.y, width='2')

    def canvasRelease(self, event):
        self.boundingBoxCounter += 1
        print(self.boundingBoxCounter)
        coords = self.canvas.coords(self.tmpBoundingBox)
        print(coords)
        self.canvas.delete(self.tmpBoundingBox)
        self.boundingBox.append(self.canvas.create_rectangle(coords[0], coords[1], coords[2], coords[3]))

    def nextButton(self):
        self.showNextImage()

    def prevButton(self):
        self.showPrevImage()

    def exitButton(self):
        Frame.quit(self)
        self.quit()

    def folderSelecter(self):
        self.working_directory = askdirectory(parent=self.parent,
                                              initialdir=r"E:\testCaseSelector\30-01-2017 18-20",
                                              title='Choose working directory')
        print(self.working_directory)

        fileListRaw = [f for f in listdir(self.working_directory) if (f.endswith(".jpg") & f[0].isdigit())]

        if len(fileListRaw) > 0:  # Check if there are files in the directory
            self.current_file = 0  # Set the current file to the first one
        else:
            # Display an error
            messagebox.showerror("Error", "Directory is empty")
            self.label_amount['text'] = "NO FILES FOUND"
            self.label_amount['foreground'] = "red"
            return

        last_file = self.current_file
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

        self.total_amount_of_images = len(fileListRaw)
        self.amount_of_processed_images = len(found_files)
        self.amount_of_images_to_process = len(self.file_list)

        self.label_amount['text'] = "{} JPG's in folder, {} already processed, {} left to process.".format(
            self.total_amount_of_images, self.amount_of_processed_images, self.amount_of_images_to_process)

        if len(self.file_list) > 0:
            filename = self.working_directory + '/' + self.file_list[self.current_file]
            print(filename)
            self.showImage(filename)
        else:
            self.showImage('placeholder.jpg')

    def showImage(self, path):
        photo = ImageTk.Image.open(path)
        photo = photo.resize((1280, 720))
        self.image = ImageTk.PhotoImage(photo)

        self.imageW = self.image.width()
        self.imageH = self.image.height()
        self.scalar = self.imageW / self.canvasW

        self.canvas.create_image(0, 0, image=self.image, anchor="nw")

    def showNextImage(self):
        # Loop through all the boxes and save them to the file
        if len(self.boundingBox) > 0:
            f = open(self.working_directory + '/' + 'output.txt', 'a')
            f.write('{},\t{:d}'.format(self.file_list[self.current_file].split('.')[0], len(self.boundingBox)))
            for box in self.boundingBox:
                coords = self.canvas.coords(box)
                x_min = min(coords[0], coords[2])
                x_max = max(coords[0], coords[2])
                y_min = min(coords[1], coords[3])
                y_max = max(coords[1], coords[3])

                w = x_max - x_min
                h = y_max - y_min

                f.write(',\t{:.0f},\t{:.0f},\t{:.0f},\t{:.0f}'.format(x_min, y_min, w, h))

            f.write('\n')
            f.close()
        else:
            f = open(self.working_directory + '/' + 'output.txt', 'a')
            f.write('{},\t{:d}'.format(self.file_list[self.current_file].split('.')[0], 0))
            f.write('\n')
            f.close()

        self.amount_of_processed_images += 1
        self.amount_of_images_to_process -= 1

        self.label_amount['text'] = "{} JPG's in folder, {} already processed, {} left to process.".format(
            self.total_amount_of_images, self.amount_of_processed_images, self.amount_of_images_to_process)

        if self.current_file + 1 < len(self.file_list):
            self.current_file = self.current_file + 1
            self.showImage(self.working_directory + '/' + self.file_list[self.current_file])
            self.boundingBoxCounter = 0
            self.boundingBox = []

            self.prev_button['state'] = 'normal'

            if self.current_file + 1 == len(self.file_list):
                self.next_button['state'] = 'disabled'
        else:
            print("End of directory, saving file")

    def showPrevImage(self):
        if self.current_file - 1 >= 0:
            self.current_file = self.current_file - 1
            self.showImage(self.working_directory + '/' + self.file_list[self.current_file])
            self.boundingBoxCounter = 0
            self.boundingBox = []

            self.next_button['state'] = 'normal'

            if self.current_file - 1 < 0:
                self.prev_button['state'] = 'disabled'
        else:
            print("Cannot find file")
