'''
Created on Jan 9, 2024

This module provides the DemoBoard class, which is the primary
entry point to all the RP2040 demo pcb functionality, including

    * pins (named, transparently muxed)
    * projects (all shuttle projects and means to enable)
    * basic utilities (auto clocking projects etc)
    

    

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''
import time
from ttdemoboard.pins import Pins, RPMode
from ttdemoboard.project_mux import ProjectMux
class DemoBoard:
    '''
        The DemoBoard object has 
         * named pins, e.g.
          print(demo.out2()) # read
          demo.in3(1) # write
          demo.uio5.mode = machine.Pin.OUT # config
          demo.uio5(1)
         * named projects
          demo.shuttle.tt_um_urish_simon.enable()
          print(demo.shuttle.tt_um_urish_simon.repo)
         
         * utilities:
          demo.resetProject(True)
          demo.clockProjectPWM(1e6) # clock it at 1MHz
          
        See below.
        
        The most obvious danger of using the RP2040 is _contention_, 
        e.g. the ASIC trying to drive out5 HIGH and the RP shorting it LOW.
        So the constructor for this class takes a mode parameter that 
        is passed to the Pins container, which must be one of the 3 modes 
        of pin init at startup.  See constructor.
        
    
    '''
    def __init__(self, mode:int=RPMode.SAFE):
        '''
            Constructor takes a mode parameter, one of:
            
             * RPMode.SAFE, the default, which has every pin as an INPUT, no pulls
             
             * RPMode.ASICONBOARD, for use with ASICs, where it watches the OUTn 
               (configured as inputs) and can drive the INn and tickle the 
               ASIC inputs (configured as outputs)
               
             * RPMode.STANDALONE: where OUTn is an OUTPUT, INn is an input, useful
               for playing with the board _without_ an ASIC onboard
               
            Choose wisely (only STANDALONE has serious contention risk)
        
        '''
        self.pins = Pins(mode=mode)
        self.shuttle = ProjectMux(self.pins)
        self._clock_pwm = None
        
        
    @property 
    def project_clk(self):
        '''
            Quick access to project clock pin.
            
            project_clk(1) # write
            project_clk.on() # same
            project_clk.toggle()
            
            all the usual pin stuff.
            
            @see: clockProject(), clockProjectPWM() and clockProjectPWMStop()
        '''
        return self.pins.rp_projclk
    
    @property 
    def project_nrst(self):
        '''
            Quick access to project clock pin.
            
            project_nrst(1) # write
            project_nrst.on() # same
            project_nrst.toggle()
            
            all the usual pin stuff.
            
            @see: resetProject()
        '''
        return self.pins.nproject_rst
    
    def resetProject(self, putInReset:bool):
        '''
            Utility to mask the logic inversion and 
            make things clear.
            
            resetProject(True) # project is in reset
            resetProject(False) # now it ain't
        '''
        if putInReset:
            self.project_nrst = False # inverted logic
        else:
            self.project_nrst = True
            
    def clockProject(self, msDelay:int=0):
        '''
            Utility method to toggle project clock 
            pin twice, optionally with a delay
            between the changes (in ms)
        '''
        self.project_clk.toggle()
        if msDelay > 0:
            time.sleep_ms(msDelay)
        self.project_clk.toggle()
        
        
    def clockProjectPWM(self, freqHz:int, duty_u16:int=(0xffff/2)):
        '''
            Start an automatic clock for the selected project (using
            PWM).
            @param freqHz: The frequency of the clocking, in Hz
            @param duty_u16: Optional duty cycle (0-0xffff), defaults to 50%  
        '''
        self.clockProjectPWMStop()
        self._clock_pwm = self.project_clk.pwm(freqHz, duty_u16)
        return self._clock_pwm
    
    def clockProjectPWMStop(self):
        '''
            Stop any started automatic project clocking.  No effect 
            if no clocking started.
        '''
        if self._clock_pwm is None:
            return 
        
        self._clock_pwm.deinit()
        self._clock_pwm = None
    
    def __getattr__(self, name):
        if hasattr(self.pins, name):
            return getattr(self.pins, name)
        raise AttributeError


