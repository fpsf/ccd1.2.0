import time

from PyQt5 import QtCore

from src.business.consoleThreadOutput import ConsoleThreadOutput
from src.business.shooters.SThread import SThread


class ContinuousShooterThread(QtCore.QThread):
    '''
    classe para modo manual
    '''

    signalAfterShooting = QtCore.pyqtSignal(name="signalAfterShooting")
    signal_temp = QtCore.pyqtSignal(name="signalTemp")

    def __init__(self, timeSleep):
        super(ContinuousShooterThread, self).__init__()
        self.continuous = True
        self.s = timeSleep

        '''
        SThread manda para o Sbigdriver as informações para se tirar a foto em si.
        '''

        self.ss = SThread()
        self.ss.started.connect(self.thread_iniciada)
        self.console = ConsoleThreadOutput()
        self.count = 0

        self.wait_temperature = False
        self.not_two_dark = True
        self.one_photo = False

    def set_sleep_time(self, t):
        self.s = t

    def run(self):
        self.count = 1
        while self.continuous:
            if not self.ss.check_connection():
                self.stop_continuous_shooter()
                continue
            try:
                self.signal_temp.emit()
                if self.wait_temperature:
                    self.ss.start()
                    while self.ss.isRunning():
                        time.sleep(1)
            except Exception as e:
                print(e)

            time.sleep(self.s)
            self.signalAfterShooting.emit()

    def start_continuous_shooter(self):
        """
        if not self.one_photo:
            self.shutter_control(True)
        """
        self.continuous = True

    def stop_continuous_shooter(self):
        if self.wait_temperature:
            self.ds.continuous = False
            self.wait_temperature = False
            self.continuous = False
            self.not_two_dark = False
            self.console.raise_text("Taking dark photo", 1)
            self.ss.take_dark()
            time.sleep(1)
            self.count = 1
        else:
            self.ds.continuous = False
            self.wait_temperature = False
            self.continuous = False
            self.not_two_dark = False
            time.sleep(1)
            self.count = 1

    def stop_one_photo(self):
        self.one_photo = False
        self.wait_temperature = False
        self.continuous = False
        self.count = 1
        self.exit()

    def thread_iniciada(self):
        if self.one_photo:
            self.console.raise_text("Taking photo", 1)
            self.stop_one_photo()
        elif self.count == 1 and not self.one_photo:
            self.console.raise_text("Taking dark photo", 1)
            self.ss.take_dark()
            self.count += 1
            self.not_two_dark = False
        elif self.count != 1 and not self.one_photo:
            self.console.raise_text("Taking photo N: {}".format(self.count), 1)
            self.count += 1

    '''
        def shutter_control(self, cont):
        try:
            ser = serial.Serial(serial_ports()[len(serial_ports()) - 1], 9600,
                                bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE)
            if cont is True:
                self.console.raise_text("Opening Shutter", 1)
                send = bytes([235, 144, 86, 1, 46])
                ser.write(send)
                # time.sleep(15)
            else:
                self.console.raise_text("Closing Shutter", 1)
                send = bytes([235, 144, 214, 1, 174])
                ser.write(send)
                # time.sleep(15)
        except Exception:
            self.console.raise_text("No Serial Equipment!", 3)

    '''

