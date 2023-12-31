# PYNQ 101

This example based on using

1. Vivado 2020.2
1. Ubuntu 18.04
1. Pynq 2.6

And with many thanks to Adam Taylor of Adiuvo Engineering whose motivational
talk and slides gave me my first introduction to practical Pynq.

[EOC_DSP project from Adiuvo](https://github.com/AdiuvoEngineering/EOC_DSP.git)

'''
git clone https://github.com/AdiuvoEngineering/EOC_DSP.git
'''

## Setup

Install Vivado using the normal Xilinx/AMD download process.  If you are lucky,
the XHub store feature will work and you can install board support for the Digitlent Pynq Z1 board directly.

If not, then clone the XilinxBoardStore, and then copy the board files into
the relevant directory. This took a while to figure out, as I assume that when
the xhub store is working correctly, the board files are cloned into 'data/xhub' and then made available to the Vivado tool chain in another way.

In this example, I copy only the Digilent board files.  The XHUB store provides parts for other vendors as well.  Note that I also used the default branch (2022.2 at time of writing) but beware minor version changes.

'''
git clone https://github.com/Xilinx/XilinxBoardStore
cp -r XilinxBoardStore/boards/Digilent $XILINX_VIVADO/data/boards/board_files
'''

## Boot the Pynq

Connect ethernet to your local network (a DHCP server is assumed to be present) and connect the USB power.

## Check the Serial Terminal

Using any serial terminal tool (I prefer gtk) connect to '/dev/ttyUSB1' with 
'115200-8-n-1' settings and check that the pynq embedded linux has booted.
Verify that an IP address has been allocated using 'ifconfig'.

## Mount the Pynq Filesystem over CIFS

Mount the pynq filesystem over CIFS. 
Copy the 'images/' and 'dsp_class/' directories from the Adiuvo repository 
to the pynq filesystem

'''
sudo mkdir /mnt/pynq
sudo mount -o username=xilinx -t cifs //pynq/xilinx
# Or if auto DNS is not working but you have figured out the pynq DHCP address
sudo mount -o username=xilinx -t cifs //ip.ip.ip.ip/xilinx
'''

## Run the iPython Notebook

Connect to 'http://ip.ip.ip.ip:9090' and open the 'dsp_class/fft.ipynb'
Work through each of the panels to see demonstration of Zynq PS and PL
implementations of FFT algorithms, including how the PS/PL interface
and what the performance differences can be.

## Create and Build the Bitstream HW



## What Just Happened ?
