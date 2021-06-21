# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sys
import datetime
sys.path.append('..')    # Should be executed from project root folder
import vscp


def test_success():
    assert vscp.VSCP_ERROR_ERROR == -1
    assert vscp.VSCP_HEADER_PRIORITY_MASK == 0xE0
    assert vscp.VSCP_HEADER16_DUMB == 32768

def test_guid():
    g1 = vscp.guid("0F:0E:0D:0C:0B:0A:09:08:07:06:05:04:03:02:01:00")
    assert isinstance(g1,object) == True
    print(g1.getAsString())
    print(g1.guid)
    g2 = vscp.guid()
    print(g2.getAsString())

def test_setDateTimeNow():
    ex = vscp.vscpEventEx()
    ex.setDateTimeNow()
    print(ex.getIsoDateTime())
    print("-------------------")

if __name__ == "__main__":
    print(datetime.datetime.utcnow())
    test_success()
    test_guid()
    test_setDateTimeNow()
    print("Everything passed")
