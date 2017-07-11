# FILE: vscphelper.py
#
# VSCP UDP functionality
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

from vscphelper import *

h1 = pyvscphlp_newSession()
if (0 == h1 ):
    pyvscphlp_closeSession(h1)
    raise ValueError('Unable to open vscphelp library session')

rv = pyvscphlp_open(h1,"127.0.0.1:9598","admin","secret")
if VSCP_ERROR_SUCCESS == rv :
    print "Command success: pyvscphlp_open on channel 1"
else:
    pyvscphlp_closeSession(h1)
    raise ValueError('Command error: pyvscphlp_open on channel 1  Error code=%d' % rv )

print "command: noop"
rv = lib.vscphlp_noop( c_ulong(h1) )
if VSCP_ERROR_SUCCESS != rv :
    pyvscphlp_closeSession(h1)
    raise ValueError('Command error: ''noop''  Error code=%d' % rv )

print "command: Get sever version"
(rv,v1,v2,v3) = pyvscphlp_getVersion(h1)
if VSCP_ERROR_SUCCESS != rv :
    pyvscphlp_closeSession(h1)
    raise ValueError('Command error: ''noop''  Error code=%d' % rv )
print "Server version = %d.%d.%d" % (v1.value,v2.value,v3.value) 

ex = vscpEventEx()
print vscpEventEx.crc
print vscpEventEx.obid
print vscpEventEx.year
print vscpEventEx.month
print vscpEventEx.day
print vscpEventEx.hour
print vscpEventEx.minute
print vscpEventEx.second
print vscpEventEx.timestamp
print vscpEventEx.head
print vscpEventEx.vscpclass
print vscpEventEx.vscptype
print vscpEventEx.guid
print vscpEventEx.sizedata
print vscpEventEx.data
#ex.timestamp = 0
ex.vscpclass = 10
ex.vscptype = 99
ex.sizedata = 3
ex.data[0] = 1
ex.data[1] = 2
ex.data[2] = 3
print "command: sendEventEx"
rv = pyvscphlp_sendEventEx(h1,ex)
if VSCP_ERROR_SUCCESS != rv :
    pyvscphlp_closeSession(h1)
    raise ValueError('Command error: sendEventEx  Error code=%d' % rv )

print "command: close"
rv = pyvscphlp_close(h1)
if VSCP_ERROR_SUCCESS != rv :
    pyvscphlp_closeSession(h1)
    raise ValueError('Command error: close  Error code=%d' % rv )

print "command: closeSession"
pyvscphlp_closeSession(h1)


#time.sleep(2)
#_ctypes.dlclose(lib._handle)
