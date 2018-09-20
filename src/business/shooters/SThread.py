import time
from datetime import datetime

import ephem
import math
from PyQt5 import QtCore

from src.business.models.image import Image
from src.controller.commons.Locker import Locker
from src.utils.camera import SbigDriver
from src.business.shooters.InfosForSThread import *


class SThread(QtCore.QThread):
    """
    Threads são fluxos de programas que executam em paralelo dentro de uma aplicação, isto é,\
    uma ramificação de uma parte da aplicação que é executada de forma independente e\
    escalonada independentemente do fluxo inicial da aplicação.
    Fonte: http://imasters.com.br/artigo/20127/py/threads-em-python/?trace=1519021197&source=single
    """
    def __init__(self):
        super(SThread, self).__init__()
        self.lock = Locker()
        self.info = []
        self.img = None
        self.generic_count = 0
        self.final_image_name = None

    @staticmethod
    def check_connection():
        return SbigDriver.getlinkstatus()

    @staticmethod
    def reconnect():
        return SbigDriver.open_driver(), SbigDriver.open_deviceusb(), SbigDriver.establishinglink()

    def take_dark(self):
        '''
        Manda instrução para o SbigDriver para tirar uma foto dark(shooter fechado)\
        com os valores na info[]
        '''
        try:
            self.set_etime_pre_binning()
            self.lock.set_acquire()
            self.info = SbigDriver.photoshoot(self.etime, self.pre, self.b, 1,
                                              self.get_axis_xi, self.get_axis_xf,
                                              self.get_axis_yi, self.get_axis_yf,
                                              self.get_ignore_crop,
                                              self.get_image_tif,
                                              self.get_image_fit)
            self.final_image_name = self.info[0] + self.info[1]
            self.init_image()
        except Exception as e:
            print(e)
        finally:
            time.sleep(1)
            self.lock.set_release()

    def set_etime_pre_binning(self):
        '''
        seta os valores para o tempo de exposição = etime, prefixo, binning, se a foto é dark ou não,\
        e valores Image contrast: bottom e top level
        '''

        try:
            info = get_camera_settings()

            self.pre = str(info[1])

            self.etime = float(info[2])
            if self.etime <= 0.12:
                self.etime = 0.12 * 100
            elif self.etime >= 3600:
                 self.etime = 3600 * 100
            else:
                self.etime = float(info[2]) * 100
            self.etime = int(self.etime)

            self.b = int(info[3])

            self.get_level1 = float(info[6])
            self.get_level2 = float(info[7])

            self.dark_photo = int(info[8])

            self.get_axis_xi = int(info[9])
            self.get_axis_xf = int(info[10])
            self.get_axis_yi = int(info[11])
            self.get_axis_yf = int(info[12])

            self.get_ignore_crop = info[13]

            self.get_image_tif = info[14]
            self.get_image_fit = info[15]


        except Exception as e:
            print(e)
            self.etime = 100
            self.b = 0
            self.dark_photo = 1
            self.get_level1 = 0.1
            self.get_level2 = 0.99

            if str(info[1]) != '':
                self.pre = str(info[1])
            else:
                self.pre = 'pre'

            self.get_axis_xi = info[9]
            self.get_axis_xf = info[10]
            self.get_axis_yi = info[11]
            self.get_axis_yf = info[12]

            self.get_ignore_crop = True

            self.get_image_tif = True
            self.get_image_fit = True

    def run(self):
        self.set_etime_pre_binning()
        self.lock.set_acquire()
        try:
            self.info = SbigDriver.photoshoot(self.etime, self.pre, self.b, self.dark_photo,
                                              self.get_axis_xi, self.get_axis_xf, self.get_axis_yi,
                                              self.get_axis_yf, self.get_ignore_crop,
                                              self.get_image_tif, self.get_image_fit)
            self.final_image_name = self.info[0] + self.info[1]
            self.init_image()
        except Exception as e:
            print(e)
        finally:
            self.lock.set_release()

    def init_image(self):
        try:
            for i in self.info:
                print(i)

            self.img = Image(self.final_image_name)
        except Exception as e:
            self.img = Image('')
        return self.img

    def get_image_info(self):
        return self.img
