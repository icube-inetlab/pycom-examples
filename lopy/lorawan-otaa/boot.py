import socket
import binascii
import pycom
import time
import os
import machine
from machine import UART
from network import WLAN
from network import LoRa

uart = UART(0, baudrate=115200)
os.dupterm(uart)

# Disable Wi-Fi
# wlan = WLAN()
# wlan.deinit()

# Disable heartbeat LED
pycom.heartbeat(False)

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN, adr=True)

# OTAA authentication parameters
# CHANGE app_eui and app_key
app_eui = binascii.unhexlify('12 34 56 78 90 12 34 56'.replace(' ',''))
app_key = binascii.unhexlify('aa bb cc dd ee ff 11 22 33 44 55 66 77 88 99 00'.replace(' ',''))

# Debug
print(os.uname())
print("DevEUI: %s" % (binascii.hexlify(lora.mac())))
print("AppEUI: %s" % (binascii.hexlify(app_eui)))
print("AppKey: %s" % (binascii.hexlify(app_key)))

# Join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0, dr=0)

# Wait until the module has joined the network
while not lora.has_joined():
    pycom.rgbled(0x140000)
    time.sleep(2.5)
    pycom.rgbled(0x000000)
    time.sleep(1.0)
    print('Not yet joined...')

print('OTAA joined')
pycom.rgbled(0x001400)
time.sleep(2.0)

# Create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# Load main file
machine.main('main.py')
