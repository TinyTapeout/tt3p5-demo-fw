from machine import Pin, Timer
import json
import time
import sys

# control
ctrl_en     = Pin(20, Pin.OUT)
ctrl_inc    = Pin(19, Pin.OUT)
ctrl_rst_n  = Pin(18, Pin.OUT)

user_clk    = Pin(21, Pin.OUT)
user_rst_n  = Pin(12, Pin.OUT)
user_in_0   = Pin(22, Pin.OUT)

user_out_0  = Pin(8,  Pin.IN)
user_out_1  = Pin(9,  Pin.IN)
user_out_2  = Pin(10, Pin.IN)
user_out_3  = Pin(11, Pin.IN)

def enable_design(name):
    with open("shuttle_index.json") as fh:
        index = json.load(fh)
        for project in index["mux"]:
            if index["mux"][project]["macro"] == name:
                count = int(project)
                repo = index["mux"][project]["repo"]
                commit = index["mux"][project]["commit"]

    try:
        print(f"enabling design {name} by sending {count} [0b{count:08b}] pulses")
        print(f"design repo {repo} @ {commit}")
    except NameError:
        print(f"no such design {name}")
        sys.exit(1)

    # reset the controller
    ctrl_inc.value(0)
    ctrl_rst_n(0)
    ctrl_en.value(0)
    time.sleep_ms(10)
    ctrl_rst_n(1)
    time.sleep_ms(10)

    # send the number of pulses required
    for c in range(count):
        ctrl_inc.value(1)
        time.sleep_ms(1)
        ctrl_inc.value(0)
        time.sleep_ms(1)

    ctrl_en.value(1)

# init
user_clk.value(0)
user_rst_n.value(0)
user_in_0.value(0)

def test_design_tnt_counter():
    # select design
    enable_design("tt_um_test")

    # reset
    user_rst_n.value(0)

    # enable the internal counter of test design
    user_in_0.value(1)
    time.sleep_ms(100)

    # take out of reset
    user_rst_n.value(1)

    # clock it forever
    while True:
        user_clk.value(0)
        time.sleep_ms(100)
        user_clk.value(1)
        time.sleep_ms(100)
        print(user_out_0.value(), user_out_1.value(), user_out_2.value(), user_out_3.value())

def test_design_loopback():
    # select design
    enable_design("tt_um_loopback")

    # toggle user in 0 forever
    while True:
        user_in_0.value(0)
        time.sleep_ms(500)
        print(user_out_0.value(), user_out_1.value(), user_out_2.value(), user_out_3.value())
        user_in_0.value(1)
        time.sleep_ms(500)
        print(user_out_0.value(), user_out_1.value(), user_out_2.value(), user_out_3.value())

def test_design_vga():
    # select design
    enable_design("tt_um_vga_clock")
    # reset
    user_rst_n.value(0)
    time.sleep_ms(1)
    user_rst_n.value(1)

    # toggle clock
    while True:
        user_clk.value(0)
        user_clk.value(1)
        print(user_out_0.value(), user_out_1.value(), user_out_2.value(), user_out_3.value())

def test_design_powergate_add():
    # select design
    enable_design("tt_um_power_test")

    # toggle user in 0 forever
    while True:
        user_in_0.value(0)
        time.sleep_ms(100)
        print(user_out_0.value(), user_out_1.value(), user_out_2.value(), user_out_3.value())
        user_in_0.value(1)
        time.sleep_ms(100)
        print(user_out_0.value(), user_out_1.value(), user_out_2.value(), user_out_3.value())

def test_design_powergate_ringosc():
    # select design
    enable_design("tt_um_ringosc_cnt_pfet")

    # toggle user in 0 forever
    while True:
        time.sleep_ms(100)
        print(user_out_0.value(), user_out_1.value(), user_out_2.value(), user_out_3.value())

if __name__ == '__main__':
#    test_design_tnt_counter()
    test_design_loopback()
#    test_design_vga()
#    test_design_powergate_add()
#    test_design_powergate_ringosc()
