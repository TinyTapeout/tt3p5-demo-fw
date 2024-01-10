# Firmware for TinyTapeout Demoboard TT3p5

PCB WIP

# Precompiled binaries

For each board rev are in [binaries](binaries).



# MicroPython SDK

The upython/ directory includes modules that implement a Python SDK, including 
the DemoBoard class which is the primary
entry point to all the TinyTapeout demo pcb's RP2040 functionality.  
This includes access to:

    * pins (named, transparently muxed)
    * projects (all shuttle projects and means to enable)
    * basic utilities (auto clocking projects etc)
    
## Quick Start

See the [README](upython/README.md) in the upython directory for all the installation and all details but as a quick start: the library allows scripts or the REPL to be used to do things like:


```
from machine import Pin
from ttdemoboard.demoboard import DemoBoard, RPMode

# get a handle to the board
demoboard = DemoBoard(RPMode.ASICONBOARD)

# enable a specific project, e.g.
demoboard.shuttle.tt_um_test.enable()

print(f'Project {demoboard.shuttle.enabled.name} running ({demoboard.shuttle.enabled.repo})')

# play with the inputs
demoboard.in0(1)
demoboard.in7(1)
# or as a byte
demoboard.input_byte = 0xAA

# start automatic project clocking
demoboard.clockProjectPWM(2e6) # clocking projects @ 2MHz


# observe some outputs
if demoboard.out2():
    print("Aha!")

print(f'Output is now {demoboard.output_byte}')

# play with bidir pins (careful)
demoboard.uio2.mode = Pin.OUT
demoboard.uio2(1) # set high

# if you changed modes on pins, like bidir, and want 
# to switch project, reset them to IN or just
demoboard.pins.reset() 
# before you switch projects

```
 


# Install requirements for tigard flasher & mpremote

    pip install -r requirements.txt

# Flash for a Caravel board

Tested on Efabless REV 5A board.

    cd tt3p5-test
    make flash_caravel
    


# License

[LICENSE](LICENSE)
