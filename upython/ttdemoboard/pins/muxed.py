'''
Created on Jan 23, 2024

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

from ttdemoboard.pins.mux_control import MuxControl
from ttdemoboard.pins.standard import StandardPin
from ttdemoboard.pins.upython import Pin

import ttdemoboard.logging as logging 
log = logging.getLogger(__name__)
class MuxedPinInfo:
    '''
        MuxedPinInfo 
        Details about a pin that is behind the 2:1 MUX
    '''
    def __init__(self, name:str, muxSelect:bool, direction):
        self.name = name 
        self.select = muxSelect
        self.dir = direction 
        
class MuxedPin(StandardPin):
    '''
        A GPIO that actually maps to two logical pins,
        through the MUX, e.g. GPIO 8 which goes through
        MUX to either cinc or out3.
        
        The purpose is to allow transparent auto-switching of mux via
        access so they will behave as the other pins in the system.
        
        E.g. reading Pins.out0() will automatically switch the MUX over
        if required before returning the read value.
        
    '''
    def __init__(self, name:str, muxCtrl:MuxControl, 
            gpio:int, pinL:MuxedPinInfo, pinH:MuxedPinInfo):
        super().__init__(name, gpio, pinH.dir)
        self.ctrl = muxCtrl
        self._currentDir = None
        
        self._muxHighPin = pinH 
        self._muxLowPin = pinL 
        
        setattr(self, self._muxHighPin.name, 
                self._pinFunc(self._muxHighPin))

        setattr(self, self._muxLowPin.name, self._pinFunc(self._muxLowPin))
        
        
    def highPin(self) -> MuxedPinInfo:
        return self._muxHighPin
    
    def lowPin(self) -> MuxedPinInfo:
        return self._muxLowPin
    
    @property 
    def currentDir(self):
        return self._currentDir
    
    @currentDir.setter 
    def currentDir(self, setTo):
        if self._currentDir == setTo:
            return 
        self._currentDir = setTo 
        self.mode = setTo
        
        log.debug(f'Set dir to {self.mode_str}')
        
    def selectPin(self, pInfo:MuxedPinInfo):
        self.ctrl.select(pInfo.select)
        self.currentDir = pInfo.dir 
        
    def _pinFunc(self, pInfo:MuxedPinInfo):
        def getsetter(value:int=None):
            self.selectPin(pInfo)
            if value is not None:
                return self.raw_pin.value(value)
            
            return self.raw_pin.value()
        
        return getsetter
    
    def _muxedChildStr(self, mpi:MuxedPinInfo):
        direction = 'OUT'
        if mpi.dir == Pin.IN:
            direction = 'IN'
        return f'{mpi.name}[{direction}]'
    
    def __repr__(self):
        return f'<MuxedPin {self.name} {self.gpio_num} ({self.mode_str}) {self._muxedChildStr(self._muxHighPin)}/{self._muxedChildStr(self._muxLowPin)}>'
    
    def __str__(self):
        return f'MuxedPin {self.name} {self.gpio_num} (now as {self.mode_str}) {self._muxedChildStr(self._muxHighPin)}/{self._muxedChildStr(self._muxLowPin)}'
