from tkinter import Tk

from GUI import GUI


def main():
    """"Run program"""
    print('Running program')

    root = Tk()
    w = 1280
    h = 720
    root.geometry("%dx%d+0+0" % (w, h))

    gui = GUI(root)

    root.mainloop()

    print('Closing program')


if __name__ == '__main__':
    main()
