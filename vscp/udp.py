# FILE: udp.py
#
# This file is part of the VSCP (http://www.vscp.org)
#
# The MIT License (MIT)
#
# Copyright (c) 2000-2017 Ake Hedman, Grodans Paradis AB <info@grodansparadis.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import struct
import socket
import sys
import datetime
from ctypes import *
from vscp import *
from PyCRC.CRCCCITT import CRCCCITT
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random

################################################################################
# Create a VSCP frame
#

def makeVscpFrame():

    # Create room for possible max frame
    frame = bytearray( 1 + \
                        VSCP_MULTICAST_PACKET0_HEADER_LENGTH + \
                        VSCP_LEVEL2_MAXDATA + \
                        2 )

    # Frame type, Type 0, unencrypted
    frame[ VSCP_MULTICAST_PACKET0_POS_PKTTYPE ] = 0

    # Head
    frame[ VSCP_MULTICAST_PACKET0_POS_HEAD_MSB ] = 0
    frame[ VSCP_MULTICAST_PACKET0_POS_HEAD_LSB ] = 0

    # Timestamp
    frame[ VSCP_MULTICAST_PACKET0_POS_TIMESTAMP ] = 0
    frame[ VSCP_MULTICAST_PACKET0_POS_TIMESTAMP + 1 ] = 0
    frame[ VSCP_MULTICAST_PACKET0_POS_TIMESTAMP + 2 ] = 0
    frame[ VSCP_MULTICAST_PACKET0_POS_TIMESTAMP + 3 ] = 0

    # UTC time
    dt = datetime.datetime.utcnow()

    # Date / time block 1956-11-02 04:23:52 GMT
    frame[ VSCP_MULTICAST_PACKET0_POS_YEAR_MSB ] = (dt.year >> 8) & 0xff
    frame[ VSCP_MULTICAST_PACKET0_POS_YEAR_LSB ] = dt.year& 0xff
    frame[ VSCP_MULTICAST_PACKET0_POS_MONTH ] = dt.month
    frame[ VSCP_MULTICAST_PACKET0_POS_DAY ] = dt.day
    frame[ VSCP_MULTICAST_PACKET0_POS_HOUR ] = dt.hour
    frame[ VSCP_MULTICAST_PACKET0_POS_MINUTE ] = dt.minute
    frame[ VSCP_MULTICAST_PACKET0_POS_SECOND ] = dt.second

    # Class = 1040 Measurement String
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_CLASS_MSB ] = 0x04
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_CLASS_LSB ] = 0x10

    # Type = Temperature = 6
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_TYPE_MSB ] = 0x00
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_TYPE_LSB ] = 0x06

    # GUID - dummy
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID ] = 0x00
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 1 ] = 0x01
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 2 ] = 0x02
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 3 ] = 0x03
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 4 ] = 0x04
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 5 ] = 0x05
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 6 ] = 0x06
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 7 ] = 0x07
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 8 ] = 0x08
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 9 ] = 0x09
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 10 ] = 0x0A
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 11 ] = 0x0B
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 12 ] = 0x0C
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 13 ] = 0x0D
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 14 ] = 0x0E
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_GUID + 15 ] = 0x0F

    # Size
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_SIZE_MSB ] = 0
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_SIZE_LSB ] = 13

    # Data  Sensor index=2, Zone=1, sunzone2", Unit=1 (Celsius)
    # Temperature = 123.45678
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA ] = 0x02        # Sensor idx = 2
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 1 ] = 0x01    # Zone = 1
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 2 ] = 0x02    # Subzone = 2
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 3 ] = 0x01    # Unit = 1 Degrees Celsius
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 4 ] = 0x31    # "1"
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 5 ] = 0x32    # "2"
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 6 ] = 0x33    # "3"
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 7 ] = 0x2E    # "."
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 8 ] = 0x34    # "4"
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 9 ] = 0x35    # "5"
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 10 ] = 0x36   # "6"
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 11 ] = 0x37   # "7"
    frame[ VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 12 ] = 0x38   # "8"

    # Calculate CRC
    frmstr = ''.join('{:02X}'.format(x) for x in frame[ 1:VSCP_MULTICAST_PACKET0_POS_VSCP_DATA + 13 ] )
    hexstr = frmstr.decode("hex")
    framecrc = CRCCCITT(version='FFFF').calculate( hexstr )

    # CRC
    frame[ 1 + VSCP_MULTICAST_PACKET0_HEADER_LENGTH + 13 ] = (framecrc >> 8) & 0xff
    frame[ 1 + VSCP_MULTICAST_PACKET0_HEADER_LENGTH + 13 + 1 ] = framecrc & 0xff

    # Shrink to frame size
    frame = frame[0: (1 + VSCP_MULTICAST_PACKET0_HEADER_LENGTH + 13 + 2 ) ]

    return frame

################################################################################
# Encrypt a VSCP frame with AES128/AES192/AES256
#

def encryptVscpFrame( frame, encryption ):

    key = binascii.unhexlify( VSCP_DEFAULT_KEY16 )
    prebyte = b"\x01"

    if  VSCP_ENCRYPTION_NONE == encryption :
        print "No encryption is used."
        return frame
    elif VSCP_ENCRYPTION_AES128 == encryption :
        print "AES128 encryption is used."
        key = binascii.unhexlify( VSCP_DEFAULT_KEY16 )
        prebyte = b"\x01"
    elif VSCP_ENCRYPTION_AES192 == encryption :
        print "AES192 encryption is used."
        key = binascii.unhexlify( VSCP_DEFAULT_KEY24 )
        prebyte = b"\x02"
    elif VSCP_ENCRYPTION_AES256 == encryption :
        print "AES256 encryption is used."
        key = binascii.unhexlify( VSCP_DEFAULT_KEY32 )
        prebyte = b"\x03"
    else :
        print "Bad encryption argument - AES128 encryption used."


    # Frame must be 16 byte aligned for encryption
    while ( len( frame ) - 1 ) % 16:
        frame.append(0)

    # Get initialization vector
    iv = Random.new().read(16)
    cipher = AES.new( key, AES.MODE_CBC, iv )
    result = prebyte  + \
        cipher.encrypt( str( frame[1:] ) ) + iv

    return result
