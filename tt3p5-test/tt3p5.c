/*
 * SPDX-FileCopyrightText: 2020 Efabless Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * SPDX-License-Identifier: Apache-2.0
 */

#include <defs.h>
#include <stub.h>
#include <hw/common.h>
#include <uart.h>
#include <uart_api.h>

#define SET(PIN,N) (PIN |=  (1<<N))
#define CLR(PIN,N) (PIN &= ~(1<<N))
#define GET(PIN,N) (PIN &   (1<<N))

// mprj_datah
//#define FW_READY    (37 - 32)
#define CTRL_EN     (32 - 32)
#define CTRL_INC    (34 - 32)
#define CTRL_RST_N  (36 - 32)
/*
#define CTRL_EN     (33 - 32)
#define CTRL_INC    (35 - 32)
#define CTRL_RST_N  (37 - 32)
*/


void delay(const int d)
{

    /* Configure timer for a single-shot countdown */
	reg_timer0_config = 0;
	reg_timer0_data = d;
    reg_timer0_config = 1;

    // Loop, waiting for value to reach zero
   reg_timer0_update = 1;  // latch current value
   while (reg_timer0_value > 0) {
           reg_timer0_update = 1;
   }

}

void configure_io()
{
    /* 
    IO Control Registers
    | DM     | VTRIP | SLOW  | AN_POL | AN_SEL | AN_EN | MOD_SEL | INP_DIS | HOLDH | OEB_N | MGMT_EN |
    | 3-bits | 1-bit | 1-bit | 1-bit  | 1-bit  | 1-bit | 1-bit   | 1-bit   | 1-bit | 1-bit | 1-bit   |

    Output: 0000_0110_0000_1110  (0x1808) = GPIO_MODE_USER_STD_OUTPUT
    | DM     | VTRIP | SLOW  | AN_POL | AN_SEL | AN_EN | MOD_SEL | INP_DIS | HOLDH | OEB_N | MGMT_EN |
    | 110    | 0     | 0     | 0      | 0      | 0     | 0       | 1       | 0     | 0     | 0       |
    
     
    Input: 0000_0001_0000_1111 (0x0402) = GPIO_MODE_USER_STD_INPUT_NOPULL
    | DM     | VTRIP | SLOW  | AN_POL | AN_SEL | AN_EN | MOD_SEL | INP_DIS | HOLDH | OEB_N | MGMT_EN |
    | 001    | 0     | 0     | 0      | 0      | 0     | 0       | 0       | 0     | 1     | 0       |

    */

    // to fix issue on 2306
    reg_mprj_io_1 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_2 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_3 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_4 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;

    // user_clock2:
    reg_mprj_io_5 =   GPIO_MODE_USER_STD_OUTPUT;
    // pad_ui_in[9:0]:
    reg_mprj_io_6 =   GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_7 =   GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_8 =   GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_9 =   GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_10 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_11 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_12 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_13 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_14 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    reg_mprj_io_15 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    // pad_uo_out[7:0]:
    reg_mprj_io_16 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_17 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_18 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_19 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_20 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_21 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_22 =  GPIO_MODE_USER_STD_OUTPUT;
    reg_mprj_io_23 =  GPIO_MODE_USER_STD_OUTPUT;
    // pad_uio_out[7:0]:
/*
    reg_mprj_io_24 =  GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_25 =  GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_26 =  GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_27 =  GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_28 =  GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_29 =  GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_30 =  GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_31 =  GPIO_MODE_USER_STD_BIDIRECTIONAL;
*/
    reg_mprj_io_24 =  GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_25 =  GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_26 =  GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_27 =  GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_28 =  GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_29 =  GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_30 =  GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_31 =  GPIO_MODE_MGMT_STD_OUTPUT;
    // ctrl_ena:
    reg_mprj_io_32 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    // ctrl_sel_inc:
    reg_mprj_io_34 =  GPIO_MODE_USER_STD_INPUT_NOPULL;
    // ctrl_sel_rst_n:
    reg_mprj_io_36 =  GPIO_MODE_USER_STD_INPUT_NOPULL;

    reg_mprj_xfer = 1;
    while (reg_mprj_xfer == 1);
    /*
    reg_mprj_io_32 =  GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_34 =  GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_36 =  GPIO_MODE_MGMT_STD_OUTPUT;
    */

}


void main()
{
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;

    configure_io();

//    SET(reg_mprj_datah, FW_READY);

    reg_la0_iena = 0x0; // input enable on for LA bank 0
    /*
    unsigned int reg_mprj_datah_temp = 0;

    // enable design 0 by sending 54 pulses
    CLR(reg_mprj_datah_temp, CTRL_INC);
    CLR(reg_mprj_datah_temp, CTRL_RST_N);
    CLR(reg_mprj_datah_temp, CTRL_EN);
    reg_mprj_datah = reg_mprj_datah_temp;
    delay(1000);
    SET(reg_mprj_datah_temp, CTRL_RST_N);
    reg_mprj_datah = reg_mprj_datah_temp;
    delay(1000);
    for(int i = 0; i < 54; i ++ )
    {
        SET(reg_mprj_datah_temp, CTRL_INC);
        reg_mprj_datah = reg_mprj_datah_temp;
        delay(1000);
        CLR(reg_mprj_datah_temp, CTRL_INC);
        reg_mprj_datah = reg_mprj_datah_temp;
        delay(1000);
    }
    SET(reg_mprj_datah_temp, CTRL_EN);
    reg_mprj_datah = reg_mprj_datah_temp;
    delay(1000);
    */

	while(1) {
        // check with the LA if the design is selected.
        reg_mprj_datal = reg_la0_data_in << 24;
        reg_gpio_out = 0x0;
        delay(1000000);
        reg_gpio_out = 0x1;
        delay(1000000);
	}
}

