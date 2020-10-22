# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import sys
sys.path.append('.')    # Should be executed from project root folder
import vscp

def test_success():
    err = vscp.VSCP_ERROR_ERROR
    print(err)
    assert True

if __name__ == "__main__":
    test_success()
    print("Everything passed")