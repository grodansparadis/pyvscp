# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sys
sys.path.append('..')    # Should be executed from project root folder
import vscp

def test_success():
    assert vscp.VSCP_ERROR_ERROR == -1
    assert vscp.VSCP_HEADER_PRIORITY_MASK == 0xE0
    assert vscp.VSCP_HEADER16_DUMB == 32768
if __name__ == "__main__":
    test_success()
    print("Everything passed")