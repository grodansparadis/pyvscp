# FILE: vscphelper.py
#
# VSCP UDP functionality
#
# This file is part of the VSCP (http://www.vscp.org)
#
# The MIT License (MIT)
#
# Copyright (c) 2000-2018 Ake Hedman, Grodans Paradis AB <info@grodansparadis.com>
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

import os
import ctypes 
import _ctypes
from vscp import *

if os.name == "nt":
    lib = cdll.LoadLibrary('libvscphelper.dll')
else:
    lib = cdll.LoadLibrary('libvscphelper.so')    

###############################################################################
# pyvscphlp_newSession
#

def pyvscphlp_newSession():
    lib.vscphlp_newSession.restype = ctypes.c_ulong
    handle = lib.vscphlp_newSession()
    return handle

###############################################################################
# pyvscphlp_closeSession
#

def pyvscphlp_closeSession( handle ):
    lib.vscphlp_closeSession( c_ulong(handle) )
    if os.name == "nt":
        _ctypes.FreeLibrary(lib1._handle)
    else:    
        _ctypes.dlclose(lib._handle)      

###############################################################################
# pyvscphlp_setResponseTimeout
#

def pyvscphlp_setResponseTimeout(handle, timeout):
    rv = lib.vscphlp_setResponseTimeout( c_ulong(handle), c_ulong(timeout) )
    return rv

###############################################################################
# pyvscphlp_setAfterCommandSleep
#

def pyvscphlp_setAfterCommandSleep(handle, timeout):
    rv = lib.vscphlp_setAfterCommandSleep( c_ulong(handle), c_ushort(timeout) )
    return rv

###############################################################################
# pyvscphlp_open
#

def pyvscphlp_open(handle,host,user,password):
    rv = lib.vscphlp_open( c_ulong(handle),
                            c_char_p(host),
                            c_char_p(user),
                            c_char_p(password))
    return rv        

###############################################################################
# pyvscphlp_openInterface
#

def pyvscphlp_openInterface(handle,interface,flags):
    rv = lib.vscphlp_openInterface( c_ulong(handle),
                                        c_char_p(interface),
                                        c_ulong(flags) )
    return rv 

###############################################################################
# pyvscphlp_close
#

def pyvscphlp_close(handle):
    rv = lib.vscphlp_close( c_ulong(handle) )
    return rv    

###############################################################################
# pyvscphlp_isConnected
#

def pyvscphlp_isConnected(handle):
    rv = lib.vscphlp_isConnected( c_ulong(handle) )
    return rv

###############################################################################
# pyvscphlp_doCommand
#

def pyvscphlp_doCommand(handle, command):
    rv = lib.vscphlp_doCommand( c_ulong(handle), c_char_p(command) )
    return rv

###############################################################################
# pyvscphlp_checkReply
#

def pyvscphlp_checkReply(handle, bClear):
    rv = lib.vscphlp_checkReply( c_ulong(handle), c_int(bClear) )
    return rv

###############################################################################
# pyvscphlp_clearLocalInputQueue
#

def pyvscphlp_clearLocalInputQueue(handle):
    rv = lib.vscphlp_clearLocalInputQueue( c_ulong(handle) )
    return rv

###############################################################################
# pyvscphlp_noop
#

def pyvscphlp_noop(handle):    
    rv = lib.vscphlp_noop( c_ulong(handle) )
    return rv  

###############################################################################
# pyvscphlp_clearDaemonEventQueue
#

def pyvscphlp_clearDaemonEventQueue(handle):    
    rv = lib.vscphlp_clearDaemonEventQueue( c_ulong(handle) )
    return rv  

###############################################################################
# pyvscphlp_sendEvent
#

def pyvscphlp_sendEvent(handle,event):    
    rv = lib.vscphlp_sendEvent( c_ulong(handle), byref(event) )
    return rv 

###############################################################################
# pyvscphlp_sendEventEx
#

def pyvscphlp_sendEventEx(handle,eventex):    
    rv = lib.vscphlp_sendEventEx( c_ulong(handle), byref(eventex) )
    return rv 

###############################################################################
# pyvscphlp_sendEvent
#

def pyvscphlp_sendEvent(handle,event):    
    rv = lib.vscphlp_sendEvent( c_ulong(handle), byref(event) )
    return rv 

###############################################################################
# pyvscphlp_receiveEvent
#

def pyvscphlp_receiveEvent(handle,event):    
    rv = lib.vscphlp_receiveEvent( c_ulong(handle), byref(event) )
    return rv 

###############################################################################
# pyvscphlp_receiveEventEx
#

def pyvscphlp_receiveEventEx(handle,eventex):    
    rv = lib.vscphlp_receiveEventEx( c_ulong(handle), byref(eventex) )
    return rv 

###############################################################################
# pyvscphlp_isDataAvailable
#

def pyvscphlp_isDataAvailable(handle,cntAvailable):    
    rv = lib.vscphlp_isDataAvailable( c_ulong(handle), byref(cntAvailable))
    return rv

###############################################################################
# pyvscphlp_enterReceiveLoop
#

def pyvscphlp_enterReceiveLoop(handle):    
    rv = lib.vscphlp_enterReceiveLoop( c_ulong(handle) )
    return rv

###############################################################################
# pyvscphlp_quitReceiveLoop
#

def pyvscphlp_quitReceiveLoop(handle):    
    rv = lib.vscphlp_quitReceiveLoop( c_ulong(handle) )
    return rv

###############################################################################
# pyvscphlp_blockingReceiveEvent
#

def pyvscphlp_blockingReceiveEvent( handle, event, timeout):    
    rv = lib.vscphlp_blockingReceiveEvent( c_ulong(handle), byref(event), c_ulong(timeout) )
    return rv 

###############################################################################
# pyvscphlp_blockingReceiveEventEx
#

def pyvscphlp_blockingReceiveEventEx( handle, eventex, timeout ):    
    rv = lib.vscphlp_blockingReceiveEventEx( c_ulong(handle), byref(eventex), c_ulong(timeout) )
    return rv 

###############################################################################
# pyvscphlp_setStatistics
#

def pyvscphlp_getStatistics( handle, statistics ):    
    rv = lib.vscphlp_getStatistics( c_ulong(handle), byref(statistics) )
    return rv 

###############################################################################
# pyvscphlp_setStatus
#

def pyvscphlp_getStatus( handle, status ):    
    rv = lib.vscphlp_getStatus( c_ulong(handle), byref(status) )
    return rv

###############################################################################
# pyvscphlp_setFilter
#

def pyvscphlp_setFilter( handle, filter ):    
    rv = lib.vscphlp_setFilter( c_ulong(handle), byref(filter) )
    return rv 

###############################################################################
# pyvscphlp_getVersion
#

def pyvscphlp_getVersion(handle):
    v1 = c_ubyte()
    v2 = c_ubyte()
    v3 = c_ubyte()
    rv = lib.vscphlp_getVersion( c_ulong(handle), byref(v1), byref(v2), byref(v3) )
    return (rv,v1,v2,v3)

###############################################################################
# pyvscphlp_getDLLVersion
#

def pyvscphlp_getDLLVersion(handle):
    dllversion = c_ulong()
    rv = lib.vscphlp_getDLLVersion( c_ulong(handle), byref( dllversion ) )
    return (rv,dllversion )

###############################################################################
# pyvscphlp_getVendorString
#

def pyvscphlp_getVendorString(handle):
    strvendor = create_string_buffer(b'\000' * 80)
    rv = lib.vscphlp_getVendorString( c_ulong(handle), strvendor, c_size_t( 80 ) )
    return (rv,repr(strvendor.value) )

###############################################################################
# pyvscphlp_getDriverInfo
#

def pyvscphlp_getDriverInfo(handle):
    strdrvinfo = create_string_buffer(b'\000' * 32000)
    rv = lib.vscphlp_getDriverInfo( c_ulong(handle), strdrvinfo, c_size_t( 32000 ) )
    return (rv,repr(strdrvinfo.value) )

###############################################################################
# pyvscphlp_vscphlp_serverShutDown
#

def pyvscphlp_vscphlp_serverShutDown(handle):
    rv = lib.vscphlp_vscphlp_serverShutDown( c_ulong(handle)  )
    return rv 
