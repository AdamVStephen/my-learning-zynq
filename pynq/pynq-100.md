# Pynq 100 : Simpler Code

Working through the pynqio example with a very basic HLS add/mul block.

Remember that the vitis_hls needs a patch y2k22 in terms of date manipulation.

Using Digitronix Nepal YouTube video 4WnFQFHrtkg plus a couple of missing steps.

1. After doing the Vivado block design and bitstream generation.
1. Export to a new folder on the pynq: the bistream file, the exported design and also the .hwh file.
1. Note the apparent need to rename all consistently.

## Commentary

The HLS tool generates getter/setter code and the associated LUT that memory maps the four I/O
between the function and an address space that the PS can see,

Using the following default code, it is possible to see how pynq can use the predictably generated
names to infer a memory mapped interface to the IP.

Python code
'''
from pynq import Overlay
overlay = Overlay('/home/xilinx/jupyter_notebooks/addmul/addmul.bit')
# Must have .hwh and .tcl in the same directory
overlay?
add_ip = overlay.addmul_0
# a = 4
add_ip.write(0x10,4)
# b = 5
add_ip.write(0x18,5)
# Read the addition result
add_ip.read(0x20)
# Read the multiplication result
add_ip.read(0x30)
'''

Resulting output.

'''
Type:        DefaultIP
String form: <pynq.overlay.DefaultIP object at 0xaee3aef0>
File:        /usr/local/lib/python3.6/dist-packages/pynq/overlay.py
Docstring:  
Driver for an IP without a more specific driver

This driver wraps an MMIO device and provides a base class
for more specific drivers written later. It also provides
access to GPIO outputs and interrupts inputs via attributes. More specific
drivers should inherit from `DefaultIP` and include a
`bindto` entry containing all of the IP that the driver
should bind to. Subclasses meeting these requirements will
automatically be registered.

Attributes
----------
mmio : pynq.MMIO
    Underlying MMIO driver for the device
_interrupts : dict
    Subset of the PL.interrupt_pins related to this IP
_gpio : dict
    Subset of the PL.gpio_dict related to this IP

9
20
'''

## Creating a Python Driver

To eliminate the tedium, a small wrapper class can be created that
provides a simpler way to read/write the memory mapped IO thus:

First from the HLS 'component.xml' we need to extract the hierarchical
IP name 
'''
  <spirit:vendor>xilinx.com</spirit:vendor>
  <spirit:library>hls</spirit:library>
  <spirit:name>addmul</spirit:name>
  <spirit:version>1.0</spirit:version>
'''

i.e. 'xilinx.com:hls:addmul:1.0'

Then

'''
from pynq import DefaultIP
class AddDriver(DefaultIP):
    def __init__(self,description):
        super().__init__(description=description)
    bindto = ['xilinx.com:hls:addmul:1.0']
    
    def add(self, a,b):
        self.write(0x10,a)
        self.write(0x18,b)
        return self.read(0x20)
    def mul(self, a,b):
        self.write(0x10,a)
        self.write(0x18,b)
        return self.read(0x30)

ol = Overlay('/home/xilinx/jupyter_notebooks/addmul/addmul.bit')
#driver=AddDriver('Simple HLS addmul demo')
#driver.add(2,2)
#driver.mult(3,3)
#ol.addmul.add(5,6)
ol?
ol.addmul_0.add(5,6)
ol.ip_dict
'''

There is a huge amount of human readable information about the HLS IP
interface as exposed through the overlay class in the ip_dict thus:

''{'addmul_0': {'addr_range': 65536,
  'device': <pynq.pl_server.device.XlnkDevice at 0xb3a9f9f0>,
  'driver': __main__.AddDriver,
  'fullpath': 'addmul_0',
  'gpio': {},
  'interrupts': {},
  'mem_id': 's_axi_control',
  'parameters': {'C_S_AXI_CONTROL_ADDR_WIDTH': '6',
   'C_S_AXI_CONTROL_BASEADDR': '0x40000000',
   'C_S_AXI_CONTROL_DATA_WIDTH': '32',
   'C_S_AXI_CONTROL_HIGHADDR': '0x4000FFFF',
   'Component_Name': 'design_1_addmul_0_0',
   'EDK_IPTYPE': 'PERIPHERAL',
   'II': 'x',
   'clk_period': '10',
   'combinational': '0',
   'latency': '3',
   'machine': '64'},
  'phys_addr': 1073741824,
  'registers': {'a': {'access': 'write-only',
    'address_offset': 16,
    'description': 'Data signal of a',
    'fields': {'a': {'access': 'write-only',
      'bit_offset': 0,
      'bit_width': 32,
      'description': 'Data signal of a'}},
    'size': 32},
   'b': {'access': 'write-only',
    'address_offset': 24,
    'description': 'Data signal of b',
    'fields': {'b': {'access': 'write-only',
      'bit_offset': 0,
      'bit_width': 32,
      'description': 'Data signal of b'}},
    'size': 32},
   'c': {'access': 'read-only',
    'address_offset': 32,
    'description': 'Data signal of c',
    'fields': {'c': {'access': 'read-only',
      'bit_offset': 0,
      'bit_width': 32,
      'description': 'Data signal of c'}},
    'size': 32},
   'c_ctrl': {'access': 'read-only',
    'address_offset': 36,
    'description': 'Control signal of c',
    'fields': {'RESERVED': {'access': 'read-only',
      'bit_offset': 1,
      'bit_width': 31,
      'description': 'Control signal of c'},
     'c_ap_vld': {'access': 'read-only',
      'bit_offset': 0,
      'bit_width': 1,
      'description': 'Control signal of c'}},
    'size': 32},
   'm': {'access': 'read-only',
    'address_offset': 48,
    'description': 'Data signal of m',
    'fields': {'m': {'access': 'read-only',
      'bit_offset': 0,
      'bit_width': 32,
      'description': 'Data signal of m'}},
    'size': 32},
   'm_ctrl': {'access': 'read-only',
    'address_offset': 52,
    'description': 'Control signal of m',
    'fields': {'RESERVED': {'access': 'read-only',
      'bit_offset': 1,
      'bit_width': 31,
      'description': 'Control signal of m'},
     'm_ap_vld': {'access': 'read-only',
      'bit_offset': 0,
      'bit_width': 1,
      'description': 'Control signal of m'}},
    'size': 32}},
  'state': None,
  'type': 'xilinx.com:hls:addmul:1.0'},
 'processing_system7_0': {'device': <pynq.pl_server.device.XlnkDevice at 0xb3a9f9f0>,
  'driver': pynq.overlay.DefaultIP,
  'parameters': {'C_DM_WIDTH': '4',
   'C_DQS_WIDTH': '4',
   'C_DQ_WIDTH': '32',
   'C_EMIO_GPIO_WIDTH': '64',
   'C_EN_EMIO_ENET0': '0',
   'C_EN_EMIO_ENET1': '0',
   'C_EN_EMIO_PJTAG': '0',
   'C_EN_EMIO_TRACE': '0',
   'C_FCLK_CLK0_BUF': 'TRUE',
   'C_FCLK_CLK1_BUF': 'FALSE',
   'C_FCLK_CLK2_BUF': 'FALSE',
   'C_FCLK_CLK3_BUF': 'FALSE',
   'C_GP0_EN_MODIFIABLE_TXN': '1',
   'C_GP1_EN_MODIFIABLE_TXN': '1',
   'C_INCLUDE_ACP_TRANS_CHECK': '0',
   'C_INCLUDE_TRACE_BUFFER': '0',
   'C_IRQ_F2P_MODE': 'DIRECT',
   'C_MIO_PRIMITIVE': '54',
   'C_M_AXI_GP0_ENABLE_STATIC_REMAP': '0',
   'C_M_AXI_GP0_ID_WIDTH': '12',
   'C_M_AXI_GP0_THREAD_ID_WIDTH': '12',
   'C_M_AXI_GP1_ENABLE_STATIC_REMAP': '0',
   'C_M_AXI_GP1_ID_WIDTH': '12',
   'C_M_AXI_GP1_THREAD_ID_WIDTH': '12',
   'C_NUM_F2P_INTR_INPUTS': '1',
   'C_PACKAGE_NAME': 'clg400',
   'C_PS7_SI_REV': 'PRODUCTION',
   'C_S_AXI_ACP_ARUSER_VAL': '31',
   'C_S_AXI_ACP_AWUSER_VAL': '31',
   'C_S_AXI_ACP_ID_WIDTH': '3',
   'C_S_AXI_GP0_ID_WIDTH': '6',
   'C_S_AXI_GP1_ID_WIDTH': '6',
   'C_S_AXI_HP0_DATA_WIDTH': '64',
   'C_S_AXI_HP0_ID_WIDTH': '6',
   'C_S_AXI_HP1_DATA_WIDTH': '64',
   'C_S_AXI_HP1_ID_WIDTH': '6','
...
...
...

'''
