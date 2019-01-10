import time
import pycom
import gc

from pytrack import Pytrack
from network import LoRa
from L76GNSS import L76GNSS

from CayenneLPP import CayenneLPP

# Enable Pytrack daughter board
py = Pytrack()
fw_version = py.read_fw_version()
print("Pytrack firmware version: " + str(fw_version))

# Enable garbage collector
gc.enable()

# Enable GPS sensor
gps = L76GNSS(py, timeout=10)

# Init LPP message buffer
lpp = CayenneLPP()

coord = None
dl_data = ""
counter = 0

while True:
    print("--LOOP")
    pycom.rgbled(0x001400)
    lpp.reset()
    lpp.add_digital_output(0, counter)
    coord = gps.coordinates()
    if coord[0] != None and coord[1] != None:
        lpp.add_gps(1, coord[0], coord[1], 0)
    else:
        print("Failed to fix GPS")
    print('Sending data (uplink)...')
    s.setblocking(True)
    s.send(bytes(lpp.get_buffer()))
    s.setblocking(False)
    pycom.rgbled(0x000000)
    dl_data = s.recv(64)
    if dl_data != "":
        print('Received data (downlink)', dl_data)
        print(lora.stats())
    counter = (counter + 1)%1024
    print('Counter', counter)
    time.sleep(20)
