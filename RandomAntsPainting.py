from PIL import ImageTk
from PIL import Image as ImagePil
from numpy import random
import tkinter
from tkinter import *
import threading
import time

# constante utilisé pour définir la taille de la fenêtre au démarrage et la taille du canvas
width_canvas = 1300
width_image = 1300
height_canvas = 600
height_image = 600


# classe qui gère les fourmis
class Fourmi:
    def __init__(self, x, y, color):

        self.x = x  # coordonnée x
        self.y = y  # coordonnée y
        self.color = color  # couleur de la fourmi
        self.lock = threading.Lock()  # un lock pour gérer la concurrence d'accès

    # fonction qui permet de déplacer une fourmi
    def deplacer(self):
        # calcul de la direction que prendra la fourmi
        direction = random.randint(0, 8, 1, 'int')

        if direction == 0:
            self.x += 0
            self.y += -1
        elif direction == 1:
            self.x += 0
            self.y += 1
        elif direction == 2:
            self.x += -1
            self.y += 0
        elif direction == 3:
            self.x += 1
            self.y += 0
        elif direction == 4:
            self.x += -1
            self.y += 1
        elif direction == 5:
            self.x += 1
            self.y += 1
        elif direction == 6:
            self.x += -1
            self.y += -1
        elif direction == 7:
            self.x += 1
            self.y += -1
        # calcule de la futur position de la fourmis
        self.x = self.x % width_image
        self.y = self.y % height_image


# Création de la fenêtre du programme
class MainWindow:
    # constructeur de la fenêtre
    def __init__(self, main):

        # Création d'un canevas pour l'image
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.image)

        # déclarer les threads
        self.thread3 = ThreadDeplacerFourmis(self)
        self.thread4 = ThreadDeplacerFourmis(self)
        self.thread2 = ThreadDeplacerFourmis(self)
        self.thread1 = ThreadDeplacerFourmis(self)

        # thread chargé du rafraichissement de l'affichage
        self.thread_update = ThreadUpdateCanvas(self)

        # set first image on canvas
        self.canvas = Canvas(main, width=width_canvas, height=height_canvas)
        self.canvas.grid(row=0, column=0)

        # l'image PIL sera utilisé pour modifié les pixels
        self.pilImage = ImagePil.new('RGB', (width_image, height_image), "WHITE")
        self.image = ImageTk.PhotoImage(self.pilImage)

        # tableau de toutes les fourmis
        self.fourmis = []
        self.nb_fourmis = 200

        # ajout d'un menu avec le bouton quitter, le bouton pour démarrer le programme et l'arrêter
        menu = Menu(main)
        menu.add_command(label="quit", command=(self.stop, main.quit))
        menu.add_command(label="start", command=self.start)
        menu.add_command(label="stop", command=self.stop)
        main.config(menu=menu)

    # démarre toutes les threads
    def start(self):

        # on essaye d'arrêter toutes les threads (dans le cas ou le programme a déjà été lancé
        # sinon on catch l'exception et on relance de nouvelle threads
        try:
            self.stop()
        except Exception:
            print("Erreur thread déjà arrêter")

        # l'image PIL sera utilisé pour modifié les pixels
        # initialisation de l'image à "blanc"
        self.pilImage = ImagePil.new('RGB', (width_image, height_image), "WHITE")
        self.image = ImageTk.PhotoImage(self.pilImage)

        for i in range(0, self.nb_fourmis):
            colorR = (random.randint(0, 255) + (i * 100)) % 255
            colorG = (random.randint(0, 255) + (i * 100)) % 255
            colorB = (random.randint(0, 255) + (i * 100)) % 255
            color = (colorR, colorG, colorB)
            # déclaration d'une fourmi avec ses coordonnées x,y et sa couleur
            self.fourmis.append(Fourmi(random.randint(0, width_image), random.randint(0, height_image), color))

        # on démarre les threads pour les fourmis
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        self.thread4.start()

        # on démarre la thread qui raffraichi l'affichage
        self.thread_update.start()

    # arrête toutes les threads
    def stop(self):

        # on essaye d'arrêter toutes les threads (dans le cas ou le programme a déjà été lancé
        # sinon on catch l'exception et on relance de nouvelle threads
        try:
            self.thread1.stop()
        except Exception:
            print("Erreur thread 1 déjà arrêter")

        try:
            self.thread2.stop()
        except Exception:
            print("Erreur thread 2 déjà arrêter")

        try:
            self.thread3.stop()
        except Exception:
            print("Erreur thread 3 déjà arrêter")

        try:
            self.thread4.stop()
        except Exception:
            print("Erreur thread 4 déjà arrêter")

        try:
            self.thread_update.stop()
        except Exception:
            print("Erreur thread update déjà arrêter")


# thread chargé d'actualisé l'affichage
class ThreadUpdateCanvas(threading.Thread):
    def __init__(self, mainWindow):
        threading.Thread.__init__(self)
        self.window = mainWindow  # on lui passe la fenêtre
        self._stop = threading.Event()  # évènement qui permettra l'arrêt de la thread
        return

    # arrête la thread
    def stop(self):
        self._stop.set()

    # permet de savoir si la thread c'est arrêté
    def stopped(self):
        return self._stop.isSet()

    def run(self):
        # tant que la thread ne s'est pas arrêté
        while not self.stopped():
            time.sleep(0.05)  # on attend 0.05 seconde
            # mise à jour de l'affichage
            self.window.image = ImageTk.PhotoImage(self.window.pilImage)
            self.window.canvas.itemconfig(self.window.image_on_canvas, image=self.window.image)
            self.window.canvas.update()


# thread chargé de déplacer toutes les fourmis
class ThreadDeplacerFourmis(threading.Thread):
    # constructeur de la thread
    def __init__(self, mainWindow):
        threading.Thread.__init__(self)
        self.window = mainWindow  # on lui passe la fenêtre afin qu'elle puise récupérer les fourmis et l'image PIL
        self._stop = threading.Event()  # évènement pour arrêté la thread
        return

    # arrête la thread
    def stop(self):
        self._stop.set()

    # permet de savoir si la thread est arrếté
    def stopped(self):
        return self._stop.isSet()

    def run(self):

        # tant que le signal d'arrêt n'est pas envoyé
        while not self.stopped():

            # on parcours les fourmis
            for i in range(0, self.window.nb_fourmis):

                fourmi = self.window.fourmis[i]
                have_it = fourmi.lock.acquire()
                try:
                    # si la fourmi n'est pas bloqué par une autre thread
                    if have_it:
                        # on déplace la fourmi
                        fourmi.deplacer()
                        # on peint un pixel de l'image la ou se trouve la fourmi
                        pixels = self.window.pilImage.load()
                        pixels[fourmi.x, fourmi.y] = fourmi.color
                finally:
                    # si le vérrou a été acqui on le libère
                    if have_it:
                        fourmi.lock.release()
        return


# lancement de la fenêtre
root = tkinter.Tk()
window = MainWindow(root)

root.mainloop()
