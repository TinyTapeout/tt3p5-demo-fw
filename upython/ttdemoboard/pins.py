'''
Created on Jan 6, 2024

Main purposes of this module are to:

  * provide named access to pins
  * provide a consistent and transparent interface 
    to standard and MUXed pins
  * provide utilities to handle logically related pins as ports (e.g. all the 
    INn pins as a list or a byte)
  * augment the machine.Pin to give us access to mode, pull etc
  * handle init sanely
  
TLDR
  1) get pins
  p = Pins(RPMode.ASICONBOARD) # monitor/control ASIC
  
  2) play with pins
  print(p.out2()) # read
  p.in3(1) # set
  p.input_byte = 0x42 # set all INn 
  p.uio1.mode = Pins.OUT # set mode
  p.uio1(1) # set output
  
  

@author: Pat Deegan
@copyright: Copyright (C) 2024 Pat Deegan, https://psychogenic.com
'''

try:
    import machine
    from machine import Pin
except:
    class Pin:
        '''
            Stub class for desktop testing,
            i.e. where machine module DNE
        '''
        OUT = 1
        IN = 2
        IRQ_FALLING = 3
        IRQ_RISING = 4
        PULL_DOWN = 5
        def __init__(self, gpio:int, direction:int):
            self.gpio = gpio
            self.dir = direction
            self.val = 0 
            
        def value(self, setTo:int = None):
            if setTo is not None:
                self.val = setTo 
            return self.val
            
        def init(self, direction:int):
            self.dir = direction


class RPMode:
    SAFE = 0
    ASICONBOARD = 1
    STANDALONE = 2


class GPIOMap:
    '''
        A place to store 
         name -> GPIO #
        along with some class-level utilities, mainly for internal use.
        
        This allows for low-level control, if you wish, e.g.
        
        myrawpin = machine.Pin(GPIOMap.OUT4, machine.Pin.OUT)
        
        The only caveat is that some of these are duplexed through 
        the MUX, and named accordingly (e.g. SDI_OUT0)
    '''
    RP_PROJCLK = 0
    HK_CSB = 1
    HK_SCK = 2
    SDI_OUT0 = 3
    SDO_OUT1 = 4
    nPROJECT_RST = 5
    CTRL_ENA = 6
    nCRST_OUT2 = 7
    CINC_OUT3 = 8
    IN0 = 9
    IN1 = 10
    IN2 = 11
    IN3 = 12
    OUT4 = 13
    OUT5 = 14
    OUT6 = 15 
    OUT7 = 16
    IN4  = 17
    IN5  = 18
    IN6  = 19
    IN7  = 20
    UIO0 = 21
    UIO1 = 22
    UIO2 = 23
    UIO3 = 24
    UIO4 = 25
    UIO5 = 26
    UIO6 = 27
    UIO7 = 28
    RPIO29 = 29
    
    @classmethod
    def muxedPairs(cls):
        mpairnames = [
            'sdi_out0',
            'sdo_out1',
            'ncrst_out2',
            'cinc_out3'
        ]
        retVals = {}
        for mpair in mpairnames:
            retVals[mpair] = mpair.split('_')
        
        return retVals;
    
    
    @classmethod 
    def muxedPinModeMap(cls, rpmode:int):
        
        pinModeMap = {
            'out0': Pin.IN,
            'out1': Pin.IN,
            'out2': Pin.IN,
            'out3': Pin.IN,
            'sdi': Pin.OUT,
            'sdo': Pin.IN,
            'ncrst': Pin.OUT,
            'cinc': Pin.OUT,
            }
        if rpmode == RPMode.STANDALONE:
            for k in pinModeMap.keys():
                if k.startswith('out'):
                    pinModeMap[k] = Pin.OUT
            
        
        return pinModeMap
        
    @classmethod 
    def always_outputs(cls):
        return [
            'nproject_rst',
            'rp_projclk',
            'ctrl_ena'
        ]
    @classmethod 
    def all(cls):
        retDict = {
            "rp_projclk": cls.RP_PROJCLK,
            "hk_csb": cls.HK_CSB,
            "hk_sck": cls.HK_SCK,
            "sdi_out0": cls.SDI_OUT0,
            "sdo_out1": cls.SDO_OUT1,
            "nproject_rst": cls.nPROJECT_RST,
            "ctrl_ena": cls.CTRL_ENA,
            "ncrst_out2": cls.nCRST_OUT2,
            "cinc_out3": cls.CINC_OUT3,
            "in0": cls.IN0,
            "in1": cls.IN1,
            "in2": cls.IN2,
            "in3": cls.IN3,
            "out4": cls.OUT4,
            "out5": cls.OUT5,
            "out6": cls.OUT6,
            "out7": cls.OUT7,
            "in4": cls.IN4,
            "in5": cls.IN5,
            "in6": cls.IN6,
            "in7": cls.IN7,
            "uio0": cls.UIO0,
            "uio1": cls.UIO1,
            "uio2": cls.UIO2,
            "uio3": cls.UIO3,
            "uio4": cls.UIO4,
            "uio5": cls.UIO5,
            "uio6": cls.UIO6,
            "uio7": cls.UIO7,
            "rpio29": cls.RPIO29
        }
        return retDict




      
class MuxedPinInfo:
    '''
        MuxedPinInfo 
        Details about a pin that is behind the 2:1 MUX
    '''
    def __init__(self, name:str, muxSelect:bool, direction):
        self.name = name 
        self.select = muxSelect
        self.dir = direction 
        
class MuxControl:
    '''
        The MUX is a 4-Bit 1-of-2, so has 4 pairs of 
        GPIO that are selected in unison by a single
        signal.
        
        The circuit is organized such that either:
         * all the outputs tied to the mux are selected; or
         * all the control signals are selected
         
        and this selector is actually the HK SPI nCS line.
        
        These facts are included here for reference, the 
        MuxControl object is actually unaware of the 
        specifics and this stuff happens either transparently
        or at higher levels
    
    '''
    def __init__(self, name:str, gpioIdx, defValue:int=1):
        self.ctrlpin = StandardPin(name, gpioIdx, Pin.OUT)
        self.ctrlpin(defValue)
        self.currentValue = defValue
        self._muxedPins = []
        
    def modeProjectIO(self):
        self.select(1)
    def modeAdmin(self):
        self.select(0)
        
    def addMuxed(self, muxd):
        self._muxedPins.append(muxd)
        
    def select(self, value:int):
        if value == self.currentValue:
            return 
        
        # set the control pin according to 
        # value.  Note that we need to make 
        # sure we switch ALL muxed pins over
        # otherwise we might end up with contention
        # as two sides think they're outputs
        # safety
        for mp in self._muxedPins:
            mp.currentDir = Pin.IN
            
        if value:
            self.ctrlpin(1)
            for mp in self._muxedPins:
                pDeets = mp.highPin()
                mp.currentDir = pDeets.dir
        else:
            self.ctrlpin(0)
            for mp in self._muxedPins:
                pDeets = mp.lowPin()
                mp.currentDir = pDeets.dir
            
        self.currentValue = value
        
    def selectHigh(self):
        self.select(1)
        
    def selectLow(self):
        self.select(0)
        
class StandardPin:
    '''
        Augmented machine.Pin
        Holds the raw machine.Pin object, provides a callable interface
          obj() # to read
          obj(1) # to write 
        and maintains/allows setting pull, mode and drive attributes
        
        # read/write attribs
        p.mode = Pin.OUT # direction
        p.pull = Pin.PULL_UP # pu
        print(p.drive) # may not be avail on any pins here, I dunno
    
    '''
    def __init__(self, name:str, gpio:int, mode:int=Pin.IN, pull:int=-1, drive:int=0):
        self._name = name
        self._mode = mode
        self._pull = pull 
        self._drive = drive 
        self._gpio_num = None
        self._pwm = None
        if isinstance(gpio, StandardPin):   
            self.raw_pin = gpio.raw_pin
            self._gpio_num = gpio.gpio_num
            self.mode = mode
        elif type(gpio) != int:
            self.raw_pin = gpio 
        else:
            self.raw_pin = Pin(gpio, mode=mode, pull=pull)
            self._gpio_num = gpio
    
    @property 
    def name(self):
        return self._name
    
    @property 
    def isInput(self):
        return self._mode == Pin.IN
    
    @property 
    def mode(self):
        return self._mode 
    
    @mode.setter 
    def mode(self, setMode:int):
        self._mode = setMode 
        self.raw_pin.init(setMode)
        
    @property 
    def mode_str(self):
        modestr = 'OUT'
        if self.isInput:
            modestr = 'IN'
        return modestr
    @property 
    def pull(self):
        return self._pull 
    
    @pull.setter 
    def pull(self, setPull:int):
        self._pull = setPull 
        self.raw_pin.init(pull=setPull)
        
    @property 
    def drive(self):
        return self._drive 
    
    @drive.setter 
    def drive(self, setDrive:int):
        self._drive = setDrive 
        self.raw_pin.init(drive=setDrive)
        
    @property 
    def gpio_num(self):
        return self._gpio_num
    
    def pwm(self, freq:int=None, duty_u16:int=None):
        if self._pwm is None:
            self._pwm = machine.PWM(self.raw_pin)
        
        if freq is not None and freq > 0:
            self._pwm.freq(int(freq))
            
        if duty_u16 is not None and duty_u16 >= 0:
            self._pwm.duty_u16(int(duty_u16))
            
        return self._pwm
        
    
    def __call__(self, value:int=None):
        if value is not None:
            return self.raw_pin.value(value)
        return self.raw_pin.value()
    
    def __getattr__(self, name):
        if hasattr(self.raw_pin, name):
            return getattr(self.raw_pin, name)
        raise AttributeError
    
    def __repr__(self):
        return f'<StandardPin {self.name} {self.gpio_num} {self.mode_str}>'
    
    def __str__(self):
        return f'Standard pin {self.name} (GPIO {self.gpio_num}), configured as {self.mode_str}'
    
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
        

class Pins:
    '''
        This object handles setup and provides uniform named
        access to all logical pins, along with some utilities.
        See below for actual direction configuration of various pins.
        
        Tab-completion in a REPL will show you all the matching 
        named attributes, and auto-complete as usual.
        
        # Pins:
        For regular read/writes to pins, access them on this object
        by name, as a function.  An empty call is a read, a call with 
        a parameter is a write.  E.g.
        
            bp = Pins(...)
            bp.out1() # reads the value
            bp.in3(1) # sets the value
            # can also use normal machine.Pin functions like
            bp.in3.off()
            # or
            bp.in3.irq(...)    
        
        Though you shouldn't need it (the pin objects support everything 
        machine.Pin does), if you want low-level access to the 
        bare machine.Pin object, it is also available by simply 
        prepending the name with "pin_", e.g.
        
            bp.pin_out1.irq(handler=whatever, trigger=Pin.IRQ_FALLING)
        
        Just beware if accessing the muxed pins (e.g. cinc_out3).
        
        # Named Ports and Utilities:
        In addition to single pin access, named ports are available for 
        input, output and bidirectional pins.
        
            bp.inputs is an array of [in0, in1, ... in7]
            bp.outputs is an array of [out0, out1, ... out7]
            bp.bidir is an array of [uio0, uio1, ... uio7]
        
        You may also access arrays of the raw machine.Pin by using _pins, e.g
            bp.input_pins
        
        Finally, the _byte properties allow you to read or set the entire 
        port as a byte
        
            print(bp.output_byte)
            # or set
            bp.input_byte = 0xAA
        
        # Pin DIRECTION
        So, from the RP2040's perspective, is out2 configured to read (an 
        input) or to write (an output)?
        
        These signals are all named according to the TT ASIC.  So, 
        under normal/expected operation, it is the ASIC that writes to OUTn 
        and reads from INn. The bidirs... who knows.
        
        What you DON'T want is contention, e.g. the ASIC trying to 
        drive out5 HIGH and the RP shorting it LOW.
        
        So this class has 3 modes of pin init at startup:
         * RPMode.SAFE, the default, which has every pin as an INPUT, no pulls
         * RPMode.ASICONBOARD, for use with ASICs, where it watches the OUTn 
           (configured as inputs) and can drive the INn and tickle the 
           ASIC inputs (configured as outputs)
         * RPMode.STANDALONE: where OUTn is an OUTPUT, INn is an input, useful
           for playing with the board _without_ an ASIC onboard
           
        To override the safe mode default, create the instance using
        p = Pins(mode=Pins.MODE_LISTENER) # for example.
        
        
        
    '''
    # convenience: aliasing here    
    IN = Pin.IN
    IRQ_FALLING = Pin.IRQ_FALLING
    IRQ_RISING = Pin.IRQ_RISING
    OPEN_DRAIN = Pin.OPEN_DRAIN
    OUT = Pin.OUT
    PULL_DOWN = Pin.PULL_DOWN
    PULL_UP = Pin.PULL_UP
    
    # MUX pin is especial...
    muxName = 'hk_csb' # special pin
    
    
    def __init__(self, mode:int=RPMode.SAFE):
        self.mode = mode
        self.muxCtrl = MuxControl(self.muxName, GPIOMap.HK_CSB, Pin.OUT)
        # special case: give access to mux control/HK nCS pin
        self.hk_csb = self.muxCtrl.ctrlpin
        self.pin_hk_csb = self.muxCtrl.ctrlpin.raw_pin 
        
        self._allpins = {'hk_csb': self.hk_csb}
        
        if mode == RPMode.STANDALONE:
            self.begin_standalone()
        elif mode == RPMode.ASICONBOARD:
            self.begin_asiconboard()
        else:
            self.begin_safe()
    
    def _pinFunc(self, p:Pin):
        def getsetter(value:int=None):
            if value is not None:
                p.value(value)
            
            return p.value()
        
        return getsetter
    
    def begin_inputs_all(self):
        
        for name,gpio in GPIOMap.all().items():
            if name == self.muxName:
                continue
            p = StandardPin(name, gpio, Pin.IN, pull=Pin.PULL_DOWN)
            setattr(self, f'pin_{name}', p.raw_pin)
            setattr(self, name, p) # self._pinFunc(p)) 
            self._allpins[name] = p
        
        return
    
    def begin_safe(self):
        self.begin_inputs_all()
        self._begin_alwaysOut()
        self._begin_muxPins()
    
    @property 
    def all(self):
        return list(self._allpins.values())
    
    def begin_asiconboard(self):
        self.begin_inputs_all()
        self._begin_alwaysOut()
        for pname in GPIOMap.all().keys():
            if pname.startswith('in'):
                p = getattr(self, pname)
                p.mode = Pin.OUT
                
        self._begin_muxPins()
        
    
    def begin_standalone(self):
        self.begin_inputs_all()
        self._begin_alwaysOut()
        
        for pname in GPIOMap.all().keys():
            if pname.startswith('out'):
                p = getattr(self, pname)
                p.mode = Pin.OUT
                
            if pname.startswith('in'):
                p = getattr(self, pname)
                p.pull = Pin.PULL_DOWN
                
        self._begin_muxPins()
        
    def _begin_alwaysOut(self):
        for pname in GPIOMap.always_outputs():
            p = getattr(self, pname)
            p.mode = Pin.OUT 
            
    def _begin_muxPins(self):
        muxedPins = GPIOMap.muxedPairs()
        modeMap = GPIOMap.muxedPinModeMap(self.mode)
        for pname, muxPair in muxedPins.items():
            mp = MuxedPin(pname, self.muxCtrl, 
                          getattr(self, pname),
                          MuxedPinInfo(muxPair[0],
                                       0, modeMap[muxPair[0]]),
                          MuxedPinInfo(muxPair[1],
                                       1, modeMap[muxPair[1]])
                          )
            self.muxCtrl.addMuxed(mp)
            self._allpins[pname] = mp
            setattr(self, muxPair[0], getattr(mp, muxPair[0]))
            setattr(self, muxPair[1], getattr(mp, muxPair[1]))
            # override bare pin attrib
            setattr(self, pname, mp)
            
    # aliases
    @property 
    def project_clk(self):
        return self.rp_projclk
    
    
    
    def list_port(self, basename:str):
        retVal = []
        
        for i in range(8):
            pname = f'{basename}{i}'
            if hasattr(self, pname):
                retVal.append(getattr(self,pname))
        
        return retVal
    
    def _read_byte(self, pinList:list):
        v = 0
        for i in range(8):
            bit = pinList[i]()
            if bit:
                v |= (1 << i)
                
        return v 
    
    def _write_byte(self, pinList:list, value:int):
        for i in range(8):
            if value & (1 << i):
                pinList[i](1)
            else:
                pinList[i](0)
    
    @property 
    def outputs(self):
        return self.list_port('out')
    
    @property 
    def output_pins(self):
        return self.list_port('pin_out')
    
    @property 
    def output_byte(self):
        return self._read_byte(self.outputs)
    
    @output_byte.setter 
    def output_byte(self, val:int):
        self._write_byte(self.outputs, val)
    
    @property 
    def inputs(self):
        return self.list_port('in')
    
    @property 
    def input_pins(self):
        return self.list_port('pin_in')
    
    @property 
    def input_byte(self):
        return self._read_byte(self.inputs)
    
    
    @input_byte.setter 
    def input_byte(self, val:int):
        self._write_byte(self.inputs, val)
    
    
    @property 
    def bidirs(self):
        return self.list_port('uio')
    
    @property 
    def bidir_pins(self):
        return self.list_port('pin_uio')
        
    @property 
    def bidir_byte(self):
        return self._read_byte(self.bidirs)
    
    @bidir_byte.setter 
    def bidir_byte(self, val:int):
        self._write_byte(self.bidirs, val)
