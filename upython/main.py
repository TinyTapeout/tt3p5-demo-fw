'''
Created on Jan 9, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

import time
from ttdemoboard.demoboard import DemoBoard, RPMode, Pins

demoboard = DemoBoard(RPMode.ASICONBOARD)
# demoboard = DemoBoard(RPMode.STANDALONE)

def autoClockProject(freqHz:int):
    demoboard.clockProjectPWM(freqHz)
    
def stopClocking():
    demoboard.clockProjectPWMStop()

def test_design_tnt_counter():
    # select the project from the shuttle
    demoboard.shuttle.tt_um_test.enable()
    
    #reset
    demoboard.nproject_rst(0)

    # enable the internal counter of test design
    demoboard.in0(1)
    time.sleep_ms(100)

    # take out of reset
    demoboard.nproject_rst(1)

    # clock it forever
    while True:
        demoboard.project_clk(0) # shortcut to demoboard.project_clk(0)
        time.sleep_ms(100)
        demoboard.project_clk(1)
        time.sleep_ms(100)
        print(hex(demoboard.output_byte & 0x0f)) # could do ...out0(), out1() etc

print("\n\n")
print("The 'demoboard' object is available.")
print()
print("Projects may be enabled with demoboard.shuttle.PROJECT_NAME.enable(), e.g.")
print("demoboard.shuttle.tt_um_urish_simon.enable()")
print()
print("Pins may be accessed by name, e.g. demoboard.out3() to read or demoboard.in5(1) to write.")
print("Config of pins may be done using mode attribute, e.g. ")
print("demoboard.uio3.mode = Pins.OUT")
print("\n\n")