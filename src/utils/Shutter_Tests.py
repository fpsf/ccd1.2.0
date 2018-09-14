import serial
from src.utils.Leitura_portas import serial_ports


def shutter_control(cont):
    if len(serial_ports()) < 1:
        print("No Serial Equipment!")
    else:
        ser = serial.Serial(serial_ports()[len(serial_ports()) - 1], 9600,
                            bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE)
        if cont is True:
            print("Opening Shutter\n")
            send = bytes([235, 144, 86, 1, 46])
            ser.write(send)
            s = ser.read(5)
            print(s)
        elif cont is None:
            print("Getting Message\n")
            send = None
            # send = bytes([235, 144, 86, 1, 46])
            ser.write(send)
            s = ser.read(5)
            print(s)
        else:
            print("Closing Shutter\n")
            send = bytes([235, 144, 214, 1, 174])
            ser.write(send)
            s = ser.read(5)
            print(s)
        '''
        except Exception:
            self.console.raise_text("No Serial Equipment!", 3)
        '''


shutter_control(False)
