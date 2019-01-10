import time
import pycom
import gc
from network import LoRa

from CayenneLPP import CayenneLPP

# Enable garbage collector
gc.enable()

dl_data = ""
counter = 0

# Init LPP message buffer
lpp = CayenneLPP()

while True:
    print("--LOOP")
    pycom.rgbled(0x001400)
    lpp.reset()
    lpp.add_digital_output(0, counter)
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
