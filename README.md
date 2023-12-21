# Firmware for TinyTapeout Demoboard TT3p5

PCB WIP

# Precompiled binaries

For each board rev are in [binaries](binaries).

# Tests

Connect an RP2040 to the [relevant pins](tt3p5-test/test.py), then:

    cd tt3p5-test
    mpremote run test.py

# Install requirements for tigard flasher & mpremote

    pip install -r requirements.txt

# Flash for a Caravel board

Tested on Efabless REV 5A board.

    cd tt3p5-test
    make flash_caravel

# License

[LICENSE](LICENSE)
