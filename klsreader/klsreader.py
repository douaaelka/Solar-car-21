import time
from pprint import pprint
from serial import Serial
from controllerdata import *
# import controllercommand  #import *
from sys import platform
from struct import *

class ControllerCommand(object):

    def __init__(self):
        self.a = '\x3A\x00\x3A'
        self.b = '\x3B\x00\x3B'


class ControllerConnector(object):
    def __init__(self, serialport):
        self.serialport = serialport

    def startSerial(self):
        self.connection = Serial(self.serialport, 19200, timeout=5)

    def getBytes(self, *commands):
        ser = self.connection
        packets = []
        for command in commands:
            ser.write(command.encode())
            # ser.write(b':\x00:')
            packet = ser.read(19)
            packets.append(packet)
        return packets

class KLSReader(object):
    def __init__(self, serialport):
        self.connector = ControllerConnector(serialport)
        self.connector.startSerial()
        self.command = ControllerCommand()

    def getData(self):
        packet_a, packet_b = self.connector.getBytes(self.command.a, self.command.b)
        data = ControllerData(packet_a, packet_b)
        return data.__dict__

if __name__ == "__main__":
    # change to the appropriate commport when running as __main__
    if platform.startswith("win"):
        serialport = 'COM4'
    else:
        serialport = '/dev/tty.usbserial-1440'

    controller = KLSReader(serialport)
    print("Connected to motor controller")

    try:
        while 1:
            data = controller.getData()
            pprint(data)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Terminating connection")
