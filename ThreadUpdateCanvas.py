import threading
import time
from PIL import ImageTk


# Thread that refresh the window
class ThreadUpdateCanvas(threading.Thread):
    def __init__(self, main_window):
        threading.Thread.__init__(self)
        self.window = main_window  # pass the main window
        self._stop = threading.Event()  # event that will stop the thread
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
            time.sleep(0.03)  # wait for 0.05 second
            # update the window display
            self.window.image = ImageTk.PhotoImage(self.window.pilImage)
            self.window.canvas.itemconfig(self.window.image_on_canvas, image=self.window.image)
            self.window.canvas.update()
