
from  vscp import *
from udp import *
from ctypes import *


e = vscpEvent()
ex = vscpEventEx()

print type(e), type(ex)

# Measurement Temperature
ex.vscpclass = 10
ex.vscptype = 6

# must use vscpEventEx not vscpEvent
frame = makeVscpFrame( 0, ex )

