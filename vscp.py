# FILE: vscp.py
#
# General VSCP functionality
#
# This file is part of the VSCP (http://www.vscp.org) 
#
# The MIT License (MIT)
# 
# Copyright (c) 2000-2020 Ake Hedman, Grodans Paradis AB <info@grodansparadis.com>
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

VSCP_DEFAULT_UDP_PORT =                 33333
VSCP_DEFAULT_TCP_PORT =                 9598
VSCP_ANNOUNCE_MULTICAST_PORT =          9598
VSCP_MULTICAST_IPV4_ADDRESS_STR =       "224.0.23.158"
VSCP_DEFAULT_MULTICAST_PORT =           44444

VSCP_DEFAULT_MULTICAST_TTL =            1

VSCP_ADDRESS_SEGMENT_CONTROLLER	=       0x00
VSCP_ADDRESS_NEW_NODE =                 0xff

#VSCP levels
VSCP_LEVEL1 =                           0
VSCP_LEVEL2 =                           1

# VSCP priority
VSCP_PRIORITY_0 =                       0x00
VSCP_PRIORITY_1 =                       0x20
VSCP_PRIORITY_2 =                       0x40
VSCP_PRIORITY_3 =                       0x60
VSCP_PRIORITY_4 =                       0x80
VSCP_PRIORITY_5 =                       0xA0
VSCP_PRIORITY_6 =                       0xC0
VSCP_PRIORITY_7 =                       0xE0

VSCP_PRIORITY_HIGH =                    0x00
VSCP_PRIORITY_LOW =                     0xE0
VSCP_PRIORITY_MEDIUM =                  0xC0
VSCP_PRIORITY_NORMAL =                  0x60

VSCP_HEADER_PRIORITY_MASK =             0xE0

VSCP_HEADER_HARD_CODED =                0x10    # If set node nickname is hardcoded
VSCP_HEADER_NO_CRC =                    0x08    # Don't calculate CRC

VSCP_NO_CRC_CALC =                      0x08    # If set no CRC is calculated

VSCP_HEADER16_DUMB                      0x8000  # This node is dumb 
VSCP_HEADER16_IPV6_GUID                 0x1000  # GUID is IPv6 address 

# Bits 14/13/12 for GUID type 
VSCP_HEADER16_GUID_TYPE_STANDARD =      0x0000  # VSCP standard GUID 
VSCP_HEADER16_GUID_TYPE_IPV6 =          0x1000  # GUID is IPv6 address 
# https://www.sohamkamani.com/blog/2016/10/05/uuid1-vs-uuid4/ */
VSCP_HEADER16_GUID_TYPE_RFC4122V1 =     0x2000      # GUID is RFC 4122 Version 1 
define VSCP_HEADER16_GUID_TYPE_RFC4122V4 = 0x3000   # GUID is RFC 4122 Version 4 

VSCP_MASK_PRIORITY =                    0xE0
VSCP_MASK_HARDCODED =                   0x10
VSCP_MASK_NOCRCCALC =                   0x08

VSCP_LEVEL1_MAXDATA =                   8
VSCP_LEVEL2_MAXDATA =                   512

VSCP_NOCRC_CALC_DUMMY_CRC =             0xAA55  # If no CRC cal bit is set the CRC value
                                                # should be set to this value for the CRC
                                                # calculation to be skipped.

VSCP_CAN_ID_HARD_CODED =	            0x02000000 # Hard coded bit in CAN frame id

# GUID byte positions
VSCP_GUID_MSB =                         0
VSCP_GUID_LSB =                         15

# Use in assignements as 'a = guidarray(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0xAA,0x55)'
guidarray = c_ubyte * 16

# VSCP event ex structure
class vscpEventEx(Structure):
    
    _fields_ = [("crc", c_uint16),
                ("obid", c_uint32),                          
                ("year", c_uint16),
                ("month", c_ubyte),
                ("day", c_ubyte),
                ("hour", c_ubyte),
                ("minute", c_ubyte),
                ("second", c_ubyte),
                ("timestamp", c_uint32),
                ("head", c_uint16),
                ("vscpclass", c_uint16),
                ("vscptype", c_uint16),
                ("guid", c_ubyte * 16),
                ("sizedata", c_uint16),
                ("data", c_ubyte * VSCP_LEVEL2_MAXDATA)] 

    def __init__(self):
        self.crc = 0
        self.obid = 0
        self.timstamp=0
        self.head =0
        dt = datetime.datetime.utcnow()
        self.year=dt.year
        self.month=dt.month
        self.day=dt.day
        self.hour=dt.hour
        self.minute=dt.minute
        self.second=dt.second
        self.vscpclass=0
        self.vscptype=0
        for i in (0,15):
            self.guid[i] = 0
        self.sizedata = 0
        for i in (0,VSCP_LEVEL2_MAXDATA-1):
            self.data[i] = 0

    def dump(self):
        print("------------------------------------------------------------------------")
        print("Dump of vscpEventEx content")
        print(" %04d-%02d-%02d %02d:%02d:%02d UTC Timestamp=%08X" % (self.year,self.month, self.day, self.hour, self.minute, self.second, self.timestamp))
        print(" head=%04X class=%d type=%d size=%d" % (self.head, self.vscpclass, self.vscptype, self.sizedata ) )
        if self.sizedata > 0:
            out = "Data = "
            for i in range(0,self.sizedata):
                out += "%02X " % self.data[i] 
            print(out)    
        else:
            print("No data.")
        print("crc=%04X obid=%08X" % (self.crc, self.obid))
        print("------------------------------------------------------------------------") 

# VSCP event structure  (!!!!! Use vscpEventEx !!!!!)
class vscpEvent(Structure):

    _fields_ = [("crc", c_uint16),
                ("obid", c_uint32),                          
                ("year", c_uint16),
                ("month", c_ubyte),
                ("day", c_ubyte),
                ("hour", c_ubyte),
                ("minute", c_ubyte),
                ("second", c_ubyte),
                ("timestamp", c_uint32),
                ("head", c_uint16),
                ("vscpclass", c_uint16),
                ("vscptype", c_uint16),
                ("guid", c_ubyte * 16),
                ("sizedata", c_uint16),
                ("pdata", POINTER(c_ubyte))]                

    def __init__(self):
        self.crc = 0
        self.obid = 0
        self.timstamp=0
        self.head =0
        self.year=0
        self.month=0
        self.day=0
        self.hour=0
        self.minute=0
        self.second=0
        self.vscpclass=0
        self.vscptype=0
        for i in (0,15):
            self.guid[i] = 0
        self.sizedata = 0
        self.pdata = None

               
   
# Receiving event filter
class vscpEventFilter(Structure):
    _fields_ = [("filter_priority", c_ubyte),
                ("mask_priority", c_ubyte),
                ("filter_class", c_ushort),
                ("mask_class", c_ushort),
                ("filter_type", c_ushort),
                ("mask_type", c_ushort),
                ("filter_guid", c_ubyte * 16),
                ("mask_guid", c_ubyte * 16) ]

    def __init__(self):
        self.filter_priority = 0
        self.mask_priority = 0
        self.filter_class = 0
        self.mask_class = 0
        self.filter_type = 0
        self.mask_type = 0
        for i in (0,15):
            self.filter_guid[i] = 0
        for i in (0,15):
            self.mask_guid[i] = 0

    def clear(self):
        self.filter_priority = 0
        self.mask_priority = 0
        self.filter_class = 0
        self.mask_class = 0
        self.filter_type = 0
        self.mask_type = 0
        for i in (0,15):
            self.filter_guid[i] = 0
        for i in (0,15):
            self.mask_guid[i] = 0

# Transmission statistics structure
class VSCPStatistics(Structure):
    _fields_ = [("cntReceiveFrames", c_ulong),
                ("cntTransmitFrames", c_ulong),
                ("cntReceiveData", c_ulong),
                ("cntTransmitData", c_ulong),
                ("cntOverruns", c_ulong),
                ("x", c_ulong),    # Placeholder
                ("y", c_ulong),    # Placeholder
                ("z", c_ulong) ]   # Placeholder

    def __init__(self):
        self.cntReceiveFrames = 0
        self.cntTransmitFrames = 0
        self.cntReceiveData = 0
        self.cntTransmitData = 0
        self.cntOverruns = 0
        self.x = 0
        self.y = 0
        self.z = 0

VSCP_STATUS_ERROR_STRING_SIZE                 =  80

# Communication channel status
class VSCPStatus(Structure):
    _fields_ = [("channel_status", c_ulong),
                ("lasterrorcode", c_ulong),
                ("lasterrorsubcode", c_ulong),
                ("lasterrorstr", c_ubyte * VSCP_STATUS_ERROR_STRING_SIZE)]

    def __init__(self):
        self.channel_status = 0
        self.lasterrorcode = 0
        self.lasterrorsubcode = 0
        for i in (0,VSCP_STATUS_ERROR_STRING_SIZE-1):
            self.lasterrorstr[i] = 0

# Communication channel info
class VSCPChannelInfo(Structure):
    _fields_ = [("channelType", c_ubyte),
                ("channel", c_ushort),
                ("guid", c_ubyte * 16)]

    def __init__(self):
        self.channelType = 0                        
        self.channel = 0
        for i in (0,15):
            self.guid[i] = 0

# VSCP Encryption types
VSCP_ENCRYPTION_NONE =                  0
VSCP_ENCRYPTION_AES128 =                1
VSCP_ENCRYPTION_AES192 =                2
VSCP_ENCRYPTION_AES256 =                3

# VSCP Encryption tokens
VSCP_ENCRYPTION_TOKEN_0 =               ""
VSCP_ENCRYPTION_TOKEN_1 =               "AES128"
VSCP_ENCRYPTION_TOKEN_2 =               "AES192"
VSCP_ENCRYPTION_TOKEN_3 =               "AES256"

# Packet frame format type = 0
#      without byte0 and CRC
#      total frame size is 1 + 34 + 2 + data-length
VSCP_MULTICAST_PACKET0_HEADER_LENGTH =      35

# Multicast packet ordinals
VSCP_MULTICAST_PACKET0_POS_PKTTYPE          = 0
VSCP_MULTICAST_PACKET0_POS_HEAD             = 1
VSCP_MULTICAST_PACKET0_POS_HEAD_MSB         = 1
VSCP_MULTICAST_PACKET0_POS_HEAD_LSB         = 2
VSCP_MULTICAST_PACKET0_POS_TIMESTAMP        = 3
VSCP_MULTICAST_PACKET0_POS_YEAR             = 7
VSCP_MULTICAST_PACKET0_POS_YEAR_MSB         = 7
VSCP_MULTICAST_PACKET0_POS_YEAR_LSB         = 8
VSCP_MULTICAST_PACKET0_POS_MONTH            = 9
VSCP_MULTICAST_PACKET0_POS_DAY              = 10
VSCP_MULTICAST_PACKET0_POS_HOUR             = 11
VSCP_MULTICAST_PACKET0_POS_MINUTE           = 12
VSCP_MULTICAST_PACKET0_POS_SECOND           = 13
VSCP_MULTICAST_PACKET0_POS_VSCP_CLASS       = 14
VSCP_MULTICAST_PACKET0_POS_VSCP_CLASS_MSB   = 14
VSCP_MULTICAST_PACKET0_POS_VSCP_CLASS_LSB   = 15
VSCP_MULTICAST_PACKET0_POS_VSCP_TYPE        = 16
VSCP_MULTICAST_PACKET0_POS_VSCP_TYPE_MSB    = 16
VSCP_MULTICAST_PACKET0_POS_VSCP_TYPE_LSB    = 17
VSCP_MULTICAST_PACKET0_POS_VSCP_GUID        = 18
VSCP_MULTICAST_PACKET0_POS_VSCP_SIZE        = 34
VSCP_MULTICAST_PACKET0_POS_VSCP_SIZE_MSB    = 34
VSCP_MULTICAST_PACKET0_POS_VSCP_SIZE_LSB    = 35
VSCP_MULTICAST_PACKET0_POS_VSCP_DATA        = 36
# Two byte CRC follow here and if the frame is encrypted
# the initialization vector follows.

# VSCP multicast packet types
VSCP_MULTICAST_TYPE_EVENT                   = 0

# Multicast proxy CLASS=1026, TYPE=3 http://www.vscp.org/docs/vscpspec/doku.php?id=class2.information#type_3_0x0003_level_ii_proxy_node_heartbeat
VSCP_MULTICAST_PROXY_HEARTBEAT_DATA_SIZE      =     192
VSCP_MULTICAST_PROXY_HEARTBEAT_POS_REALGUID   =     0       # The real GUID for the node
VSCP_MULTICAST_PROXY_HEARTBEAT_POS_IFGUID     =     32      # GUID for interface node is on
VSCP_MULTICAST_PROXY_HEARTBEAT_POS_IFLEVEL    =     48      # 0=Level I node, 1=Level II node
VSCP_MULTICAST_PROXY_HEARTBEAT_POS_NODENAME   =     64      # Name of node
VSCP_MULTICAST_PROXY_HEARTBEAT_POS_IFNAME     =     128     # Name of interface

# Default key for VSCP Server
# Change if other key is used
VSCP_DEFAULT_KEY16 = 'A4A86F7D7E119BA3F0CD06881E371B98'
VSCP_DEFAULT_KEY24 = 'A4A86F7D7E119BA3F0CD06881E371B989B33B6D606A863B6'
VSCP_DEFAULT_KEY32 = 'A4A86F7D7E119BA3F0CD06881E371B989B33B6D606A863B633EF529D64544F8E'

# Bootloaders
VSCP_BOOTLOADER_VSCP          =         0x00	# VSCP boot loader algorithm
VSCP_BOOTLOADER_PIC1          =         0x01	# PIC algorithm 0
VSCP_BOOTLOADER_AVR1          =         0x10	# AVR algorithm 0
VSCP_BOOTLOADER_LPC1          =         0x20	# NXP/Philips LPC algorithm 0
VSCP_BOOTLOADER_ST            =         0x30	# ST STR algorithm 0
VSCP_BOOTLOADER_FREESCALE     =         0x40	# Freescale Kinetics algorithm 0
VSCP_BOOTLOADER_NONE          =         0xff

#          * * * Data Coding for VSCP packets * * *

# Data format masks
VSCP_MASK_DATACODING_TYPE     =         0xE0  # Bits 5,6,7
VSCP_MASK_DATACODING_UNIT     =         0x18  # Bits 3,4
VSCP_MASK_DATACODING_INDEX    =         0x07  # Bits 0,1,2

# These bits are coded in the three MSB bytes of the first data byte
# in a packet and tells the type of the data that follows.
VSCP_DATACODING_BIT           =         0x00
VSCP_DATACODING_BYTE          =         0x20
VSCP_DATACODING_STRING        =         0x40
VSCP_DATACODING_INTEGER       =         0x60
VSCP_DATACODING_NORMALIZED    =         0x80
VSCP_DATACODING_SINGLE        =         0xA0  # single precision float
VSCP_DATACODING_DOUBLE        =         0xC0  # double precision float
VSCP_DATACODING_RESERVED2     =         0xE0

# These bits are coded in the four least significant bits of the first data byte
# in a packet and tells how the following data should be interpreted. For a flow sensor
# the default format can be litres/minute. Other formats such as m3/second can be defined 
# by the node if it which. However it must always be able to report in the default format.
VSCP_DATACODING_INTERPRETION_DEFAULT  =  0

# CRC8 Constants
VSCP_CRC8_POLYNOMIAL          =         0x18
VSCP_CRC8_REMINDER            =         0x00

# CRC16 Constants
VSCP_CRC16_POLYNOMIAL         =         0x1021
VSCP_CRC16_REMINDER           =         0xFFFF

# CRC32 Constants
VSCP_CRC32_POLYNOMIAL         =         0x04C11DB7
VSCP_CRC32_REMINDER           =         0xFFFFFFFF


# Node data - the required registers are fetched from this 
#	structure
class vscpMyNode(Structure):
    _fields_ = [ ("guid", c_ubyte * 16),
                 ("nicknameID", c_ubyte ) ]

# * * * Standard VSCP registers * * *

# Register defines above 0x7f
VSCP_STD_REGISTER_ALARM_STATUS              =   0x80

VSCP_STD_REGISTER_MAJOR_VERSION             =   0x81
VSCP_STD_REGISTER_MINOR_VERSION             =   0x82
VSCP_STD_REGISTER_SUB_VERSION               =   0x83

# 0x84 - 0x88
VSCP_STD_REGISTER_USER_ID                   =   0x84

# 0x89 - 0x8C
VSCP_STD_REGISTER_USER_MANDEV_ID            =   0x89

# 0x8D -0x90
VSCP_STD_REGISTER_USER_MANSUBDEV_ID         =   0x8D

# Nickname
VSCP_STD_REGISTER_NICKNAME_ID               =   0x91

# Selected register page
VSCP_STD_REGISTER_PAGE_SELECT_MSB           =   0x92
VSCP_STD_REGISTER_PAGE_SELECT_LSB           =   0x93

# Firmware version
VSCP_STD_REGISTER_FIRMWARE_MAJOR            =   0x94
VSCP_STD_REGISTER_FIRMWARE_MINOR            =   0x95
VSCP_STD_REGISTER_FIRMWARE_SUBMINOR         =   0x96

VSCP_STD_REGISTER_BOOT_LOADER               =   0x97
VSCP_STD_REGISTER_BUFFER_SIZE               =   0x98
VSCP_STD_REGISTER_PAGES_COUNT               =   0x99

# 0xd0 - 0xdf  GUID
VSCP_STD_REGISTER_GUID                      =   0xD0
 
# 0xe0 - 0xff  MDF
VSCP_STD_REGISTER_DEVICE_URL                =   0xE0

# Level I Decision Matrix
VSCP_LEVEL1_DM_ROW_SIZE                     =   8

VSCP_LEVEL1_DM_OFFSET_OADDR                 =   0
VSCP_LEVEL1_DM_OFFSET_FLAGS                 =   1
VSCP_LEVEL1_DM_OFFSET_CLASS_MASK            =   2
VSCP_LEVEL1_DM_OFFSET_CLASS_FILTER          =   3
VSCP_LEVEL1_DM_OFFSET_TYPE_MASK             =   4
VSCP_LEVEL1_DM_OFFSET_TYPE_FILTER           =   5
VSCP_LEVEL1_DM_OFFSET_ACTION                =   6
VSCP_LEVEL1_DM_OFFSET_ACTION_PARAM          =   7

# Bits for VSCP server 64/16-bit capability code
# used by CLASS1.PROTOCOL, HIGH END SERVER RESPONSE
# and low end 16-bits for
# CLASS2.PROTOCOL, HIGH END SERVER HEART BEAT

VSCP_SERVER_CAPABILITY_TCPIP                =   (1<<15)
VSCP_SERVER_CAPABILITY_UDP                  =   (1<<14)
VSCP_SERVER_CAPABILITY_MULTICAST_ANNOUNCE   =   (1<<13)
VSCP_SERVER_CAPABILITY_RAWETH               =   (1<<12)
VSCP_SERVER_CAPABILITY_WEB                  =   (1<<11)
VSCP_SERVER_CAPABILITY_WEBSOCKET            =   (1<<10)
VSCP_SERVER_CAPABILITY_REST                 =   (1<<9)
VSCP_SERVER_CAPABILITY_MULTICAST_CHANNEL    =   (1<<8)
VSCP_SERVER_CAPABILITY_RESERVED             =   (1<<7)
VSCP_SERVER_CAPABILITY_IP6                  =   (1<<6)
VSCP_SERVER_CAPABILITY_IP4                  =   (1<<5)
VSCP_SERVER_CAPABILITY_SSL                  =   (1<<4)
VSCP_SERVER_CAPABILITY_TWO_CONNECTIONS      =   (1<<3)
VSCP_SERVER_CAPABILITY_AES256               =   (1<<2)
VSCP_SERVER_CAPABILITY_AES192               =   (1<<1)
VSCP_SERVER_CAPABILITY_AES128               =   1

# Offsets into the data of the capabilities event
# VSCP_CLASS2_PROTOCOL, Type=20/VSCP2_TYPE_PROTOCOL_HIGH_END_SERVER_CAPS
VSCP_CAPABILITY_OFFSET_CAP_ARRAY            =   0
VSCP_CAPABILITY_OFFSET_GUID                 =   8
VSCP_CAPABILITY_OFFSET_IP_ADDR              =   24
VSCP_CAPABILITY_OFFSET_SRV_NAME             =   40
VSCP_CAPABILITY_OFFSET_NON_STD_PORTS        =   104

# Error Codes
VSCP_ERROR_SUCCESS                          =   0       # All is OK
VSCP_ERROR_ERROR                            =   -1      # Error
VSCP_ERROR_CHANNEL                          =   7       # Invalid channel
VSCP_ERROR_FIFO_EMPTY                       =   8       # FIFO is empty
VSCP_ERROR_FIFO_FULL                        =   9       # FIFI is full
VSCP_ERROR_FIFO_SIZE                        =   10      # FIFO size error
VSCP_ERROR_FIFO_WAIT                        =   11      
VSCP_ERROR_GENERIC                          =   12      # Generic error
VSCP_ERROR_HARDWARE                         =   13      # Hardware error
VSCP_ERROR_INIT_FAIL                        =   14      # Initialization failed
VSCP_ERROR_INIT_MISSING                     =   15
VSCP_ERROR_INIT_READY                       =   16
VSCP_ERROR_NOT_SUPPORTED                    =   17      # Not supported
VSCP_ERROR_OVERRUN                          =   18      # Overrun
VSCP_ERROR_RCV_EMPTY                        =   19      # Receive buffer empty
VSCP_ERROR_REGISTER                         =   20      # Register value error
VSCP_ERROR_TRM_FULL                         =   21      # Transmit buffer full
VSCP_ERROR_LIBRARY                          =   28      # Unable to load library
VSCP_ERROR_PROCADDRESS                      =   29      # Unable get library proc. address
VSCP_ERROR_ONLY_ONE_INSTANCE                =   30      # Only one instance allowed
VSCP_ERROR_SUB_DRIVER                       =   31      # Problem with sub driver call
VSCP_ERROR_TIMEOUT                          =   32      # Time-out
VSCP_ERROR_NOT_OPEN                         =   33      # The device is not open.
VSCP_ERROR_PARAMETER                        =   34      # A parameter is invalid.
VSCP_ERROR_MEMORY                           =   35      # Memory exhausted.
VSCP_ERROR_INTERNAL                         =   36      # Some kind of internal program error
VSCP_ERROR_COMMUNICATION                    =   37      # Some kind of communication error
VSCP_ERROR_USER                             =   38      # Login error user name
VSCP_ERROR_PASSWORD                         =   39      # Login error password
VSCP_ERROR_CONNECTION                       =   40      # Could not connect   
VSCP_ERROR_INVALID_HANDLE                   =   41      # The handle is not valid
VSCP_ERROR_OPERATION_FAILED                 =   42      # Operation failed for some reason
VSCP_ERROR_BUFFER_TO_SMALL                  =   43      # Supplied buffer is to small to fit content
VSCP_ERROR_UNKNOWN_ITEM                     =   44      # Requested item (remote variable) is unknown
VSCP_ERROR_ALREADY_DEFINED                  =   45      # The name is already in use.
VSCP_ERROR_WRITE_ERROR                      =   46      # Error when writing data 
VSCP_ERROR_STOPPED                          =   47      # Operation stopped or aborted 
VSCP_ERROR_INVALID_POINTER                  =   48      # Pointer with invalid value 
VSCP_ERROR_INVALID_PERMISSION               =   49      # Not allowed to do that 
VSCP_ERROR_INVALID_PATH                     =   50      # Invalid path (permissions) 
VSCP_ERROR_ERRNO                            =   51      # General error, errno variable holds error 
VSCP_ERROR_INTERUPTED                       =   52      # Interupted by signal or other cause 
VSCP_ERROR_MISSING                          =   53      # Value, paramter or something else is missing 
VSCP_ERROR_NOT_CONNECTED                    =   54      # There is no connection 

#
#    Template for VSCP XML event data
# 
#    data: datetime,head,obid,datetime,timestamp,class,type,guid,sizedata,data,note
#  
#
# EXAMPLE
# <event
#     vscpHead="3"
#     vscpObId="1234"
#     vscpDateTime="2017-01-13T10:16:02"
#     vscpTimeStamp="50817"
#     vscpClass="10"
#     vscpType="6"
#     vscpGuid="00:00:00:00:00:00:00:00:00:00:00:00:00:01:00:02"
#     vscpData="0x48,0x34,0x35,0x2E,0x34,0x36,0x34" />
# 
VSCP_XML_EVENT_TEMPLATE = "<event\n"\
    "vscpHead=\"%d\"\n"\
    "vscpObId=\"%lu\"\n"\
    "vscpDateTime=\"%s\"\n"\
    "vscpTimeStamp=\"%lu\"\n"\
    "vscpClass=\"%d\"\n"\
    "vscpType=\"%d\"\n"\
    "vscpGuid=\"%s\"\n"\
    "vscpSizeData=\"%d\"\n"\
    "vscpData=\"%s\"\n"\
    "vscpNote=\"%s\"\n"\
"/>"

#
#  
#    Template for VSCP JSON event data
#    data: datetime,head,obid,datetime,timestamp,class,type,guid,data,note 
#  
#    EXAMPLE
#    "vscpHead": 2,
#    "vscpObId"; 123,
#    "vscpDateTime": "2017-01-13T10:16:02",
#    "vscpTimeStamp":50817,
#    "vscpClass": 10,
#    "vscpType": 8,
#    "vscpGuid": "00:00:00:00:00:00:00:00:00:00:00:00:00:01:00:02",
#    "vscpData": [1,2,3,4,5,6,7],
#    "vscpNote": "This is some text"
#
#
VSCP_JSON_EVENT_TEMPLATE = "{\n"\
    "\"vscpHead\": %d,\n"\
    "\"vscpObId\":  %lu,\n"\
    "\"vscpDateTime\": \"%s\",\n"\
    "\"vscpTimeStamp\": %lu,\n"\
    "\"vscpClass\": %d,\n"\
    "\"vscpType\": %d,\n"\
    "\"vscpGuid\": \"%s\",\n"\
    "\"vscpData\": [%s],\n"\
    "\"vscpNote\": \"%s\"\n"\
"}"

#
# 
#    Template for VSCP HTML event data  
#   
#    data: datetime,class,type,data-count,data,guid,head,timestamp,obid,note
# 
#<h2>VSCP Event</h2>
#<p>
#    Time: 2017-01-13T10:16:02 <br>
#</p>
#<p>
#    Class: 10 <br>
#    Type: 6 <br>
#</p>
#<p>
#    Data count: 6<br>
#    Data: 1,2,3,4,5,6,7<br>
#</p>
#<p>
#    From GUID: 00:00:00:00:00:00:00:00:00:00:00:00:00:01:00:02<br>
#</p>
#<p>
#    Head: 6 <br>
#    DateTime: 2013-11-02T12:34:22Z
#    Timestamp: 1234 <br>
#    obid: 1234 <br>
#    note: This is a note <br>
#</p>
# 

VSCP_HTML_EVENT_TEMPLATE = "<h2>VSCP Event</h2> "\
    "<p>"\
    "Class: %d <br>"\
    "Type: %d <br>"\
    "</p>"\
    "<p>"\
    "Data count: %d<br>"\
    "Data: %s<br>"\
    "</p>"\
    "<p>"\
    "From GUID: %s<br>"\
    "</p>"\
    "<p>"\
    "Head: %d <br>"\
    "<p>"\
    "DateTime: %s <br>"\
    "</p>"\
    "Timestamp: %lu <br>"\
    "obid: %lu <br>"\
    "note: %s <br>"\
    "</p>"

# Set packet type part of multicast packet type
def SET_VSCP_MULTICAST_TYPE( type, encryption ) :     
    return ( ( type << 4 ) | encryption )

# Get packet type part of multicast packet type
def GET_VSCP_MULTICAST_PACKET_TYPE( type) :   
    return ( ( type >> 4 ) & 0x0f )

# Get encryption part if multicast packet type
def GET_VSCP_MULTICAST_PACKET_ENCRYPTION( type ) :     
    return ( ( type ) & 0x0f )

# Get data coding type
def VSCP_DATACODING_TYPE( b ) :
    return ( VSCP_MASK_DATACODING_TYPE & b )

# Get data coding unit
def VSCP_DATACODING_UNIT( b ) :
    return ( ( VSCP_MASK_DATACODING_UNIT & b ) >> 3 )

# Get data coding sensor index
def VSCP_DATACODING_INDEX( b ) :
    return ( VSCP_MASK_DATACODING_INDEX & b )


################################################################################
# Encapsulate the VSCP GUID
#

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

    def setGUIDFromMAC(self, id=0):
        self.guid = self.getArrayFromString('FF:FF:FF:FF:FF:FF:FF:FE:' + \
  	                            getmac.get_mac_address().upper() + \
  	                            ":{0:02X}:{1:02X}".format(int(id/256),id & 0xff))



