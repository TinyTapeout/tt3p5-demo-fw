'''
Created on Jan 9, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''
import ttdemoboard.util.time as time
from ttdemoboard.mode import RPMode
from ttdemoboard.demoboard import DemoBoard

# Pin import to provide access in REPL
# to things like demoboard.uio3.mode = Pin.OUT
from ttdemoboard.pins.upython import Pin

demoboard = None
def startup():
    global demoboard
    
    # construct DemoBoard
    # either pass an appropriate RPMode, e.g. RPMode.ASIC_ON_BOARD
    # or have "mode = ASIC_ON_BOARD" in ini DEFAULT section
    demoboard = DemoBoard()

    
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

def autoClockProject(freqHz:int):
    demoboard.clockProjectPWM(freqHz)
    
def stopClocking():
    demoboard.clockProjectPWMStop()

def test_design_tnt_counter():
    # select the project from the shuttle
    demoboard.shuttle.tt_um_test.enable()
    
    #reset
    demoboard.resetProject(True)

    # enable the internal counter of test design
    demoboard.in0(1)

    # take out of reset
    demoboard.resetProject(False)
    
    print('Running tt_um_test, printing output...Ctrl-C to stop')
    time.sleep_ms(300)
    
    demoboard.clockProjectPWM(10)
    try:
        while True:
            print(hex(demoboard.output_byte & 0x0f)) # could do ...out0(), out1() etc
            time.sleep_ms(100)
    except KeyboardInterrupt:
        demoboard.clockProjectPWMStop()
        
def test_bidirs():
    # select the project from the shuttle
    demoboard.shuttle.tt_um_test.enable()
    curMode = demoboard.mode 
    demoboard.mode = RPMode.ASIC_ON_BOARD # make sure we're controlling everything
    
    demoboard.in0(0) # want this low
    demoboard.clockProjectPWM(1e3) # clock it real good
    
    for bp in demoboard.bidirs:
        bp.mode = Pin.OUT
        bp(0) # start low
    
    errCount = 0
    for i in range(0xff):
        demoboard.bidir_byte = i 
        time.sleep_ms(1)
        outbyte = demoboard.output_byte
        if outbyte !=  i:
            print(f'MISMATCH between bidir val {i} and output {outbyte}')
            errCount += 1
    
    if errCount:
        print(f'{errCount} ERRORS encountered??!')
    else:
        print('Bi-directional pins acting pretty nicely as inputs!')
        
    # reset everything
    demoboard.mode = curMode
            
    

def test_neptune():
    demoboard.shuttle.tt_um_psychogenic_neptuneproportional.enable()
    for i in range(20, 340, 10):
        demoboard.in5.pwm(i)
        time.sleep_ms(1000)
        print(f'Input at {i}Hz, outputs are {hex(demoboard.output_byte)}')
    
    demoboard.in5.pwm(0) # disable pwm

startup()
#demoboard.shuttle.tt_um_test.enable()
#demoboard.shuttle.tt_um_psychogenic_neptuneproportional.enable()
print(demoboard)


