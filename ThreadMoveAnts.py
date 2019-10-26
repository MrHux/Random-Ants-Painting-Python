import threading


# Thread that will move Ants
class ThreadMoveAnts(threading.Thread):
    def __init__(self, main_window):
        threading.Thread.__init__(self)
        self.window = main_window  # pass the main window so it can access ants and PIL image
        self._stop = threading.Event()  # event to stop the thread
        return

    # stop the thread
    def stop(self):
        self._stop.set()

    # check if the thread is being stopped
    def stopped(self):
        return self._stop.isSet()

    def run(self):
        # while the stop signal isn't send
        while not self.stopped():

            # browse the ant
            for i in range(0, self.window.nb_ants):

                ant = self.window.ants[i]
                have_it = ant.lock.acquire()
                try:
                    # if the ant isn't locked by another thread
                    if have_it:
                        # move the ant
                        ant.deplacer()
                        # draw the pixel where the ant is
                        pixels = self.window.pilImage.load()
                        pixels[ant.x, ant.y] = ant.color
                finally:
                    # if the lock has been acquired, we release it
                    if have_it:
                        ant.lock.release()
        return
