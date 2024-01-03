#!/usr/bin/env python3

from pynq import Overlay

from pynq import DefaultIP

class AddMul(DefaultIP):
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

for (a,b) in [[2,2],[3,3],[4,4],[1024,1024], [2**32-1,2], [2**32-1,4], [2**32-1,8]]:
    print("Add %d + %d = %d\n" % (a, b, ol.addmul_0.add(a,b)))
    print("Mul %d * %d = %d\n" % (a, b, ol.addmul_0.mul(a,b)))

print("And that's all folks")

