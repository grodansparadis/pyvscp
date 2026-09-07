# Tests for the 64-bit unix ns timestamp functionality in vscp.py

import sys
import os
import time
import types
import datetime

# Make sure the local vscp.py wins over any installed pyvscp
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import getmac  # noqa: F401
except ImportError:
    # Stub, only needed by guid.setGUIDFromMAC which is not tested here
    sys.modules['getmac'] = types.ModuleType('getmac')

import vscp


def test_convert_ns_to_datetime():
    # 2017-01-13T10:16:02Z + 50817 us + 873 ns
    ns = 1484302562050817873
    dt, ts = vscp.convertNsTimestampToDateTime(ns)
    assert dt == datetime.datetime(2017, 1, 13, 10, 16, 2)
    assert ts == 50817

def test_convert_datetime_to_ns():
    dt = datetime.datetime(2017, 1, 13, 10, 16, 2)
    ns = vscp.convertDateTimeToNsTimestamp(dt, 50817)
    assert ns == 1484302562050817000

def test_convert_datetime_to_ns_default_timestamp():
    dt = datetime.datetime(1970, 1, 1)
    assert vscp.convertDateTimeToNsTimestamp(dt) == 0

def test_convert_roundtrip():
    ns = time.time_ns()
    dt, ts = vscp.convertNsTimestampToDateTime(ns)
    back = vscp.convertDateTimeToNsTimestamp(dt, ts)
    # Resolution below one microsecond is lost
    assert back == (ns // 1000) * 1000

def test_event_ns_timestamp_roundtrip():
    for ev in (vscp.vscpEventEx(), vscp.vscpEvent()):
        ns = 1484302562050817000
        ev.setFromNsTimestamp(ns)
        assert (ev.year, ev.month, ev.day) == (2017, 1, 13)
        assert (ev.hour, ev.minute, ev.second) == (10, 16, 2)
        assert ev.timestamp == 50817
        assert ev.getNsTimestamp() == ns

def test_event_setDateTimeNow():
    ex = vscp.vscpEventEx()
    before = time.time_ns()
    ex.setDateTimeNow()
    after = time.time_ns()
    assert (before // 1000) * 1000 <= ex.getNsTimestamp() <= after

def test_setTimestamp_is_subsecond_microseconds():
    ex = vscp.vscpEventEx()
    ex.setTimestamp()
    assert 0 <= ex.timestamp < 1000000

def test_toJSON_uses_ns_timestamp():
    for ev in (vscp.vscpEventEx(), vscp.vscpEvent()):
        j = ev.toJSON()
        assert j["vscpTimestampns"] == ev.getNsTimestamp()
        assert "vscpDateTime" not in j
        assert "vscpTimeStamp" not in j

def test_toString_contains_ns_timestamp():
    ex = vscp.vscpEventEx()
    ex.setFromNsTimestamp(1484302562050817000)
    assert "1484302562050817000" in ex.toString()

def test_json_template_uses_ns_timestamp():
    assert "vscpTimestampns" in vscp.VSCP_JSON_EVENT_TEMPLATE
    assert "vscpDateTime" not in vscp.VSCP_JSON_EVENT_TEMPLATE
    assert "vscpTimeStamp" not in vscp.VSCP_JSON_EVENT_TEMPLATE

def test_xml_html_templates_use_ns_timestamp():
    assert "vscpTimestampns" in vscp.VSCP_XML_EVENT_TEMPLATE
    assert "vscpDateTime" not in vscp.VSCP_XML_EVENT_TEMPLATE
    assert "Timestampns" in vscp.VSCP_HTML_EVENT_TEMPLATE
    assert "DateTime" not in vscp.VSCP_HTML_EVENT_TEMPLATE


if __name__ == "__main__":
    test_convert_ns_to_datetime()
    test_convert_datetime_to_ns()
    test_convert_datetime_to_ns_default_timestamp()
    test_convert_roundtrip()
    test_event_ns_timestamp_roundtrip()
    test_event_setDateTimeNow()
    test_setTimestamp_is_subsecond_microseconds()
    test_toJSON_uses_ns_timestamp()
    test_toString_contains_ns_timestamp()
    test_json_template_uses_ns_timestamp()
    test_xml_html_templates_use_ns_timestamp()
    print("Everything passed")
