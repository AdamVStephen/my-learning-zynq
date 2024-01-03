# PMOD DAC Project

The pynq sources and standard Z1 SD card image provides support for the Digilent DA4 pmod device. The implementation is via a short C program that targets a MicroBlaze soft core.

A copy of the source code for the SPI implementation of the interface is provided in this directory
for reference.

The goal of the project is to adapt this (or use directly if practical) to drive the DA2 pmod device.

## SPI Refresh

The SPI protocol provides for a four wire full duplex serial bus with a master/slave clocked data transfer.  The bus master sets the chip select line low to initiate addressing and data transmission.

In each clock cycle, full duplex bit exchange occurs with the two wires for data being MOSI and MISO  (Master Out/Slave In or Master In/Slave Out).  Not all devices need use full duplex.

In a 'multi-drop' design, separate chip select lines can be provided to sub devices which all share the data bus.  In a daisy chain design, successive subordinate devices can chain their data.

## DA4 Hardware

From the DA4 device driver documentation, the DA4 is an 8 channel 12 bit DAC implemented
on an AD5628 chip.  [Digilent docs](http://store.digilentinc.com/pmodda4-eight-12-bit-d-a-outputs/).  The AD5628 chip has around 14 pins of which 5 are broken out to provide the SPI protocol
and power.  Power and ground take two pins.  Chip-select, MOSI and clock take the other three.  There is no MISO since the DAC provides no handshake and only needs to receive data.

The DAC has a 512 deep sample FIFO with a maximum SCLK frequency of 50MHz.  The full functionality of the device is described in the AD data sheet including the register model for controlling the chip behaviour, power state and other functions.

## DA4 PMod Driver Code

Taking the pmod microblaze pynq example (pmod_dac.c) this uses an SPI library to open a 
device handle.  According to a command mode, the number of channels to be used is set up.
 A mailbox interface between the PS and PL manages updates and/or arbitrary waveform
generation.

A wrapper function switches between alternative kinds of waveform, each of which 
can be triggered to iterate a number of repeat cycles with a delay (or not)
between each cycle.

At the core of each waveform function there is an SPI transfer of a fixed data
there are 4 control bytes, two of which are fixed, two of which have a mix of control
data and channel data.

The main control loop is provided by a main function (and hence the driver interface is as a long running service daemon, with a mailbox interface for modifying the control while it is running.

The Pynq python interface provides the binding between the PynqMicroblaze generic pattern for using MicroBlaze soft core
microprocessors to drive lower level peripherals.  This instantiates a Microblaze processor which loads and runs the
main control loop.  The python interface handles changes to the mailbox interfaces to get functionality changes
within the running control program.

The first exercise is therefore to create a variant of the DA4 driver for the DA2 and to provide a different
python wrapper to that code.

As a secondary exercise, it is proposed to modify the pynq code to expose more of the built-in functionality
within the DA4 driver.

A useful skillset would be to work out how to launch the processes from other types of software.

Whether it is possible to put FreeRTOS or similar on to a separate Microblaze processor so as to be 
able to interact with the driver program more directly from the APU Linux is an interesting question.

It may be possible to achieve this within the EPS32 or Arduino context more simply.

## DA2 

The DA2 module looks much more basic with two very small ICs each with only 6 pins. 
[Digilent docs](https://digilent.com/reference/pmod/pmodda2/start) confirms that it is only a two channel device, and it is operated via GPIO.  It can drive outputs at up to 16.5MSa.  The pinout uses 6 pins, with power/ground, a clock, a sync (chip select) and two data lines.  The protocol is also described as SPI-like.  Later research identifies the ICs as NS DAC121S101

The data is sent in chunks of 16 bits which comprise 2 bits not used (MSB), 2 bits for power mode (normal/1kOhm/100kOhm/High Z), 12 bits for data.  The output voltage is established on pims P1 and P3 of the J2 output connector.

For microcontroller (arduino reference example) a reference PMOD application in arduino format is provided using the Arduino library SPI library.  It sets the clock at 1MHz (16MHz/16) and a data mode of SPI_MODE3.  In the 'loop' a value to send is obtained, two byte values are computed and then transferred sequentially.   Interestingly the code sample is in French (and a comment on the linked project suggests the code is incorrect, though maybe a good start).

Example code for "MPIDE" is provided (MPIDE is a multi-platform extension of Arduino).	The C++ code is very similar to the Arduino example.  There is also some pin setup.  It also uses a default 1MHz SPI frequency.

Example VHXL code for an "XBOARD" (CPLD device) is provided.  The project data sheet explains that the PMOD chips are National Semiconductor DAC121S101 D/A converters which have 12 bit data and 8us settling time (which suggests a maximum output bandwith of 125kHz).

So this simple device is a good model for developing hardware code and comparing the maximum performance achievable using microcontroller SPI interface versus direct VHDL SPI interface.

The VHD code is very directly an implementation of the clocking and chip select management.  The provided  interface where the data comes in also needs a clock and interface to drive the registers in some higher level overall application (or to expose the data in to Pynq say).

All in all - a nice and very simple project, and we can test the DA2 module simply from an Arduino or comparable device (ESP32 perhaps?).


