import time

from PyQt5 import QtCore

from src.controller.camera import Camera


class QThreadTemperature(QtCore.QThread):
    temp_signal = QtCore.pyqtSignal(str, name="temperatureSignal")

    def __init__(self):
        super(QThreadTemperature, self).__init__()
        self.cam = Camera()
        self.temperatura = "None"

    def run(self):
        while True:
            time.sleep(2)
            self.temperatura = self.cam.get_temperature()[0]
            if self.temperatura != "None":
                self.temperatura = "{0:.2f}".format(float(self.temperatura))
                self.temp_signal.emit(self.temperatura)
