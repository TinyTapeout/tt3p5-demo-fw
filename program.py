#!/usr/bin/env python3
import os


DeviceURI = 'ftdi://ftdi:2232:TG110925/2'
while True:
    input("Press enter to flash")
    os.system(f"python3 flasher/flash_util.py  --uri {DeviceURI} --write binaries/v2.2.3.bin") 
