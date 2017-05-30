# 8-Bit Breadboard Emulator #

Copyright 2017 Al Brown

al [at] eartoearoak.com

An emulation of [Ben Eater's 8-bit breadboard computer](https://eater.net/8bit/).

This software is in the beta stage and it's functionality may change as more videos are released.

Further information can be found on the [website](https://eartoearoak.com/software/ebbbe)

## Installation ##
This software requires [Python 2.7.x](https://www.python.org/)which is installed by default on most Linux distributions, Windows users can follow the download link and for Mac users I recommend using [MacPorts](https://www.macports.org/).

Once Python is setup run the following command:

`pip install -U ebbbe`

This command can also be used to update the software to the latest version.

The source code is available on [GitHub](https://github.com/EarToEarOak/ebbbe).

## Usage ##
At a command prompt run:

`ebbbe_start.py`

The emulator boots-up with an example program to calculate the Fibonacci Sequence, to start it click the 'Run' button.

#### Running Programs ####
1. First load a program using File->Open or pressing Ctrl-O.  Programs are stored in a 16 byte binary file - these can be created using a hex editor.
2. Start the clock by clicking Run or pressing Ctrl-R, pressing it again will stop the clock.  You can manually step through the program using the Step button.  The dial can be used to speed up the clock, at faster speeds the interface LEDs may not be updated until a HLT instruction is executed to prevent the user interface from becoming unresponsive.

#### Resetting ####
- Soft Reset - Resets all the registers and flags but leaves the RAM contents intact.
- Hard Reset - Resets everything including the data in RAM.

#### Viewing the Memory ####
The memory can be viewed by navigating to View->RAM or pressing Ctrl-M.

The RAM window displays the address, contents and disassembly of the memory along with the locations that the program counter (PC) and memory address register (MAR) point to.

## Instruction Set ##
| Instruction | Hex | Description                                          |
|-------------|------|-----------------------------------------------------|
| **nop**     | 0x00 | No operation                                        |
| **lda** i   | 0x1i | Load A with the value at location i                 |
| **add** i   | 0x2i | Add the value at location i to A, store in A        |
| **sub** i   | 0x3i | Subtract the value at location i from A, store in A |
| **sta** i   | 0x4i | Store the value in A at location i                  |
| **jmp** i   | 0x5i | Jump to location i                                  |
| **ldi** i   | 0x7i | Load A with the value i                             |
| **jc**  i   | 0x8i | Not currently implemented                           |
| **out**     | 0xe0 | Load OUT with A                                     |
| **hlt**     | 0xf0 | Halt execution                                      | 
           


## License ##

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation version 2.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

