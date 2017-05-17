from tkinter import Tk, Frame, BOTH

from GUI import GUI

def main():
    """"Run program"""
    print('Running program')

    root = Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.geometry("%dx%d+0+0" % (w, h))

    gui = GUI(root)

    root.mainloop()

    print('Closing program')


if __name__ == '__main__':
    main()
