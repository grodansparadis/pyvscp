
from vscp import *
from udp import *
from ctypes import *

def makeClass2StrMeasurement( vscpclass, vscptype, strval ):
    ex = vscpEventEx()
    return ex

e = vscpEvent()
ex = vscpEventEx()

print type(e), type(ex)

ex.head = 0

# Measurement Temperature str
ex.vscpclass = VSCP_CLASS2_MEASUREMENT_STR
ex.vscptype = VSCP_TYPE_MEASUREMENT_TEMPERATURE
ex.sizedata = 2
ex.dump()

# Temperature
temperature = "27.235"
#temperature = -22.872
b = bytearray()
b.extend(temperature)
print int(temperature[0].encode("hex")), len(b)
ex = makeClass2StrMeasurement( 1, 2, temperature )


# must use vscpEventEx not vscpEvent
frame = makeVscpFrame( 0, ex )

