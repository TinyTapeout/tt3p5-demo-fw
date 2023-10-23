#include <defs.h>
//#include <math.h>
#include <stub.h>
#include <hw/common.h>
#include <uart.h>
#include <uart_api.h>

// --------------------------------------------------------
// Firmware routines
// --------------------------------------------------------

void configure_io()
{

    //  GPIO 0 is turned off to prevent toggling the debug pin; For debug, make this an output and
    //  drive it externally to ground.

    reg_mprj_io_0 = GPIO_MODE_MGMT_STD_ANALOG;

    // Changing configuration for IO[1-4] will interfere with programming flash. if you change them,
    // You may need to hold reset while powering up the board and initiating flash to keep the process
    // configuring these IO from their default values.

    // https://github.com/TinyTapeout/tinytapeout-02/blob/tt02/INFO.md#pinout

    reg_mprj_io_1 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_2 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_3 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_4 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;

    // design select
    reg_mprj_io_12 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_13 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_14 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_15 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_16 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_17 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_18 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_19 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_20 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;

    // inputs
    reg_mprj_io_21 = GPIO_MODE_MGMT_STD_INPUT_PULLUP;
    reg_mprj_io_22 = GPIO_MODE_MGMT_STD_INPUT_PULLUP;
    reg_mprj_io_23 = GPIO_MODE_MGMT_STD_INPUT_PULLUP;
    reg_mprj_io_24 = GPIO_MODE_MGMT_STD_INPUT_PULLUP;
    reg_mprj_io_25 = GPIO_MODE_MGMT_STD_INPUT_PULLUP;
    reg_mprj_io_26 = GPIO_MODE_MGMT_STD_INPUT_PULLUP;
    reg_mprj_io_27 = GPIO_MODE_MGMT_STD_INPUT_PULLUP;
    reg_mprj_io_28 = GPIO_MODE_MGMT_STD_INPUT_PULLUP;

    // pins for the 7 seg counter
    reg_mprj_io_29 = GPIO_MODE_USER_STD_OUTPUT; 
    reg_mprj_io_30 = GPIO_MODE_USER_STD_OUTPUT; 
    reg_mprj_io_31 = GPIO_MODE_USER_STD_OUTPUT; 
    reg_mprj_io_32 = GPIO_MODE_USER_STD_OUTPUT; 
    reg_mprj_io_33 = GPIO_MODE_USER_STD_OUTPUT; 
    reg_mprj_io_34 = GPIO_MODE_USER_STD_OUTPUT; 
    reg_mprj_io_35 = GPIO_MODE_USER_STD_OUTPUT; 
    reg_mprj_io_36 = GPIO_MODE_USER_STD_OUTPUT; 
    
    // ready
    reg_mprj_io_37 = GPIO_MODE_USER_STD_OUTPUT; 

    // slow clock
    reg_mprj_io_10 = GPIO_MODE_USER_STD_OUT_MONITORED; 

    // set slow clock divider
    reg_mprj_io_11 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN; 

    // drive sel, 00 external, 01 LA, 1x internal
    reg_mprj_io_9 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN;
    reg_mprj_io_8 = GPIO_MODE_MGMT_STD_INPUT_PULLDOWN; 

    // Initiate the serial transfer to configure IO
    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1);
}


void main()
{
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;

    configure_io();

    // flash along with the slow clock
    while (true)
    {
        reg_gpio_out = (reg_mprj_datal >> 10) & 0x1;
    }
}
