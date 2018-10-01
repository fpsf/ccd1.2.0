from PyQt5 import QtWidgets

from src.controller.camera import Camera
from src.controller.commons.Locker import Locker


class TempRegulation(QtWidgets.QWidget):
    lock = Locker()

    def __init__(self, parent=None):
        super(TempRegulation, self).__init__(parent)
        self.cam = Camera()

        self.setBtn = QtWidgets.QPushButton("Set Temp.", self)
        self.setBtn.clicked.connect(self.btn_temperature)

        self.setField = QtWidgets.QLineEdit(self)

        # self.setLayout(set_hbox(self.setBtn, self.setField))

    def btn_temperature(self):
        try:
            value = self.setField.text()
            if value is not '':
                self.cam.set_temperature(float(value))
        except Exception as e:
            print("Exception -> {}".format(e))
