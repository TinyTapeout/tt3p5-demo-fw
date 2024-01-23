'''
Created on Jan 9, 2024

Deprecated low-level testing of boards

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

import time
from ttboard.pins import Pins, RPMode

p = Pins(RPMode.STANDALONE)

resetTriggered = False
def resetClick(p):
    global resetTriggered 
    resetTriggered = True 
    print('nRESET click!')
    
def didReset():
    global resetTriggered 
    if resetTriggered:
        resetTriggered = False 
        return True
    
    return False
    

def toggleOutputs():
    
    for o in p.outputs:
        if didReset():
            return False
        o(1)
        time.sleep(0.15)
    
    time.sleep(0.2)
    
    for o in p.outputs:
        if didReset():
            return False 
        o(0)
        time.sleep(0.15)
    
    return True 

def loopOutputs():
    global resetTriggered
    resetTriggered = False
    while toggleOutputs():
        pass 
    
    for o in p.outputs:
        o(0)
    

def inputChanged(_pn):
    print(f'Input changed! Now {hex(p.input_byte)}')
    
p.nproject_rst.irq(resetClick, Pins.IRQ_FALLING)
for ip in p.inputs:
    ip.irq(inputChanged, Pins.IRQ_FALLING|Pins.IRQ_RISING)

