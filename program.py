#!/usr/bin/env python3
import os

while True:
    input("Press enter to flash")
    os.system(f"python3 flasher/flash_util.py  --write binaries/v2.2.3.bin") 
