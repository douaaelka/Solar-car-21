import time
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from klsreader.klsreader import KLSReader

commport = '/dev/tty.usbserial-1440'

controller = KLSReader(commport)

print("Connected to motor controller\n")

Dict = controller.getData()
while 1 :
    print(Dict)
#to read any specific data, print Dict['Name of that data']
