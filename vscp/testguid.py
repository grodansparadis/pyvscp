
import vscp
from ctypes import *


class guid:
    
    def __init__(self):
        self.clear()

    def getArrayFromString(self, guidstr):
        g = tuple(int(z,16) for z in guidstr.split(':'))
        return ((c_ubyte * 16)(*g))

    def setFromString(self, guidstr):
        self.guid = self.getArrayFromString(guidstr)

    def getAsString(self):
        sa = [format("%02X" % a) for a in self.guid]
        return ( ":" . join(sa))

    def reverse(self):
        self.guid = self.guid[::-1]

    def clear(self):
        self.setFromString("00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00")

    def getAt(self,pos):
        return self.guid[pos]

    def setAt(self,pos,value):
        self.guid[pos] = value

    def getLSB(self):
        return self.guid[15]

    def setLSB(self,value):
        self.guid[15] = value

    def getNickname(self):
        return self.guid[15]

    def setNickname(self, value):
        self.guid[15] = value   

    def getNicknameID(self):
        return ((self.guid[14]<<8) + self.guid[15])

    def setNicknameID(self,nicknameid):
        self.guid[14] = ((nicknameid >> 8) & 0xff)
        self.guid[15] = (nicknameid & 0xff)    

    def getClientID(self):
        return ((self.guid[12]<<8) + self.guid[13])

    def setClientID(self,clientid):
        self.guid[12] = ((clientid >> 8) & 0xff)
        self.guid[13] = (clientid & 0xff)

    def isSame(self,arr):
        if 16 > len(arr): return False 
        for i in range(0, 15):
            if ( self.guid[i] != arr[i] ):
                return False
        return True

    def isNULL(self):
        return (0 == sum(self.guid))

# GUID conversion
gg = guid()
print "After creation:", gg.getAsString()

gg.setFromString("00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF")
print "guid = ", gg.getAsString()

gg.reverse()
print "reverse guid = ", gg.getAsString()
print "guid[2] = ", gg.getAt(2), format("%02X" % gg.getAt(2))

gg.setAt(2,33)
print "setat(2,33) guid[2] = ", gg.getAt(2), format("%02X" % gg.getAt(2))

print "LSB = ", gg.getLSB(), format("%02X" % gg.getLSB())
gg.setLSB(12)
print "setLSB(12) LSB = ", gg.getLSB(), format("%02X" % gg.getLSB())

print "setLSB(12) LSB = ", gg.getNickname(), format("%02X" % gg.getNickname())

print "Nickname = ", format("%02X" % gg.getNickname()), "Nickname ID", format("%04X" % gg.getNicknameID())

gg.setNickname(99)
print "After setNickname (99) - Nickname = ", format("%02X" % gg.getNickname()), "Nickname ID", format("%04X" % gg.getNicknameID())

gg.setNicknameID(0xaa55)
print "After setNicknameID (0xAA55) - Nickname = ", format("%02X" % gg.getNickname()), "Nickname ID", format("%04X" % gg.getNicknameID())

gg.clear()
print "After clear() guid = ", gg.getAsString()
print "isNULL() = ", gg.isNULL()
gg.setNicknameID(0xaa55)
print "(False) isNULL() = ", gg.isNULL()

print "(False) isSame() = ", \
    gg.isSame( gg.getArrayFromString("99:99:99:00:00:00:00:00:00:00:00:10:10:10:10:00"))

print "guid = ", gg.getAsString()
print "(True) isSame() = ", \
    gg.isSame( gg.getArrayFromString("00:00:00:00:00:00:00:00:00:00:00:00:00:00:AA:55"))    

a = vscp.guidarray(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0xAA,0x55)
b = vscp.guidarray(11,0,0,0,0,0,0,0,0,0,0,0,0,0,0xAA,0x55)

print "(True) isSame() = ", gg.isSame(a)
print "(False) isSame() = ", gg.isSame(b)


