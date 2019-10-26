from PIL import ImageTk
from PIL import Image as ImagePil
from numpy import random
from tkinter import *
from Ant import Ant
from conf import width_canvas, width_image, height_canvas, height_image

from ThreadMoveAnts import ThreadMoveAnts
from ThreadUpdateCanvas import ThreadUpdateCanvas


# Define the main window of the program
class MainWindow:
    def __init__(self, main):

        self.main = main

        # set first image on canvas
        self.canvas = Canvas(main, width=width_canvas, height=height_canvas)
        self.canvas.grid(row=0, column=0)

        self.pilImage = ImagePil.new('RGB', (width_image, height_image), "WHITE")
        self.image = ImageTk.PhotoImage(self.pilImage)

        # Array of all ants
        self.ants = []
        self.nb_ants = 200

        # Create a canvas for the image
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.image)

        # create all thread that will compute ant's movements
        self.thread3 = None
        self.thread4 = None
        self.thread2 = None
        self.thread1 = None

        # thread that will manage window's refresh
        self.thread_update = None

        # add a menu with button quit, start and stop
        menu = Menu(main)
        menu.add_command(label="quit", command=self.quit)
        menu.add_command(label="start", command=self.start)
        menu.add_command(label="stop", command=self.stop)
        main.config(menu=menu)

    # Starts all threads
    def start(self):

        # First stop all thread (in case the program is already started) else start new threads
        try:
            self.stop()
        except Exception:
            print("Error thread already stopped")

        # the PIL image will be use to show the ants movements, we use it to change the pixels
        # we initialize the image will white pixels
        self.pilImage = ImagePil.new('RGB', (width_image, height_image), "WHITE")
        self.image = ImageTk.PhotoImage(self.pilImage)

        # for each ants associate a random color and random position
        for i in range(0, self.nb_ants):
            colorR = (random.randint(0, 255) + (i * 100)) % 255
            colorG = (random.randint(0, 255) + (i * 100)) % 255
            colorB = (random.randint(0, 255) + (i * 100)) % 255
            color = (colorR, colorG, colorB)
            # create the ants with the new color and random position
            self.ants.append(Ant(random.randint(0, width_image), random.randint(0, height_image), color))

        # Create a canvas for the image
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.image)

        # create all thread that will compute ant's movements
        self.thread3 = ThreadMoveAnts(self)
        self.thread4 = ThreadMoveAnts(self)
        self.thread2 = ThreadMoveAnts(self)
        self.thread1 = ThreadMoveAnts(self)

        # thread that will manage window's refresh
        self.thread_update = ThreadUpdateCanvas(self)

        # start thread that will compute ants movements
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        self.thread4.start()

        # start the window's refresh thread
        self.thread_update.start()

    # stop all threads
    def stop(self):
        try:
            self.thread1.stop()
        except Exception:
            print("Error thread 1 already stopped")

        try:
            self.thread2.stop()
        except Exception:
            print("Error thread 2 already stopped")

        try:
            self.thread3.stop()
        except Exception:
            print("Error thread 3 already stopped")

        try:
            self.thread4.stop()
        except Exception:
            print("Error thread 4 already stopped")

        try:
            self.thread_update.stop()
        except Exception:
            print("Error window's refresh thread already stopped")

    # stop the program thread and close the window
    def quit(self):
        self.stop()
        self.main.destroy()
