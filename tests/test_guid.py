# Tests for parsing all GUID string forms described in the VSCP specification
# https://grodansparadis.github.io/vscp-doc-spec/#/./vscp_globally_unique_identifiers

import sys
import os
import types

# Make sure the local vscp.py wins over any installed pyvscp
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import getmac  # noqa: F401
except ImportError:
    # Stub, only needed by guid.setGUIDFromMAC which is not tested here
    sys.modules['getmac'] = types.ModuleType('getmac')

import vscp


def as_list(g):
    return list(g.guid)


def test_full_colon_form():
    g = vscp.guid("0F:0E:0D:0C:0B:0A:09:08:07:06:05:04:03:02:01:00")
    assert as_list(g) == list(range(15, -1, -1))

def test_lower_case():
    g = vscp.guid("ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:01")
    assert as_list(g) == [0xFF] * 15 + [0x01]

def test_grouped_colon_form():
    # Groups may hold more than one byte
    g = vscp.guid("0F0E:0D0C:0B:0A:09:08:07:06:05:04:03:02:01:00")
    assert as_list(g) == list(range(15, -1, -1))

def test_zero_fill_shorthand():
    g = vscp.guid("::1")
    assert as_list(g) == [0] * 15 + [0x01]

def test_zero_fill_infix():
    g = vscp.guid("FF:21::22:32")
    assert as_list(g) == [0xFF, 0x21] + [0] * 12 + [0x22, 0x32]

def test_zero_fill_multibyte_group():
    g = vscp.guid("::0102:03aa:44:01:30")
    assert as_list(g) == [0] * 9 + [0x01, 0x02, 0x03, 0xAA, 0x44, 0x01, 0x30]

def test_null_guid_shorthands():
    assert as_list(vscp.guid("::")) == [0] * 16
    assert as_list(vscp.guid("-")) == [0] * 16
    assert vscp.guid("-").isNULL()

def test_dash_colon_zero_fill():
    g = vscp.guid("-:1,2,3")
    assert as_list(g) == [0] * 13 + [0x01, 0x02, 0x03]

def test_ff_fill_shorthand():
    g = vscp.guid("*:1")
    assert as_list(g) == [0xFF] * 15 + [0x01]

def test_trailing_zero_fill():
    expected = [0x01] + [0] * 15
    assert as_list(vscp.guid("01:-")) == expected
    assert as_list(vscp.guid("01::")) == expected
    assert as_list(vscp.guid("01")) == expected

def test_trailing_ff_fill():
    expected = [0x01] + [0xFF] * 15
    assert as_list(vscp.guid("01*")) == expected
    assert as_list(vscp.guid("01:*")) == expected

def test_compact_short_form():
    g = vscp.guid("001122")
    assert as_list(g) == [0x00, 0x11, 0x22] + [0] * 13

def test_registry_form_with_braces():
    g = vscp.guid("{FFFFFFFF-FFFF-FFFF-0102-03AABB440130}")
    assert as_list(g) == [0xFF] * 8 + [0x01, 0x02, 0x03, 0xAA, 0xBB, 0x44, 0x01, 0x30]

def test_registry_form_without_braces():
    g = vscp.guid("FFFFFFFF-FFFF-FFFF-0102-03AABB440130")
    assert as_list(g) == [0xFF] * 8 + [0x01, 0x02, 0x03, 0xAA, 0xBB, 0x44, 0x01, 0x30]

def test_broadcast_registry_form():
    # Note: the spec example "FFFFFFFF-FFFF-FFFF-FFFF-FFFF-FFFF-FFFF-FFFF"
    # holds 18 bytes and is malformed; standard 8-4-4-4-12 grouping used here
    g = vscp.guid("FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF")
    assert as_list(g) == [0xFF] * 16

def test_plain_hex_form():
    g = vscp.guid("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF01")
    assert as_list(g) == [0xFF] * 15 + [0x01]

def test_ipv6_style_word_groups():
    g = vscp.guid("2001:0db8:0000:0000:0000:0000:0000:0001")
    assert as_list(g) == [0x20, 0x01, 0x0D, 0xB8] + [0] * 10 + [0x00, 0x01]

def test_setFromString():
    g = vscp.guid()
    g.setFromString("::5")
    assert as_list(g) == [0] * 15 + [0x05]

def test_spec_document_examples():
    ZEROS = ":".join(["00"] * 16)
    FFS = ":".join(["FF"] * 16)
    # Every (shorthand, full GUID) example from the specification document
    cases = [
        # Prose examples
        ("FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:01",
         "FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:01"),
        ("ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:ff:01",
         "FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:01"),
        ("*:1", "FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:01"),
        ("::1", "00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:01"),
        ("::0102:03aa:44:01:30",
         "00:00:00:00:00:00:00:00:00:01:02:03:AA:44:01:30"),
        ("FF-FF-FF-FF-FFFF-FFFF-0102-03AABB-440130",
         "FF:FF:FF:FF:FF:FF:FF:FF:01:02:03:AA:BB:44:01:30"),
        ("FFFFFFFF-FFFF-FFFF-0102-03-AA-BB-440130",
         "FF:FF:FF:FF:FF:FF:FF:FF:01:02:03:AA:BB:44:01:30"),
        ("FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF", FFS),
        ("00000000-0000-0000-0000-000000000000", ZEROS),
        # Examples table
        ("00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF",
         "00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF"),
        ("00112233445566778899AABBCCDDEEFF",
         "00:11:22:33:44:55:66:77:88:99:AA:BB:CC:DD:EE:FF"),
        ("-", ZEROS),
        ("::", ZEROS),
        ("*", FFS),
        ("*:0102:03aa:44:01:30",
         "FF:FF:FF:FF:FF:FF:FF:FF:FF:01:02:03:AA:44:01:30"),
        ("-:0102:03aa:44:01:30",
         "00:00:00:00:00:00:00:00:00:01:02:03:AA:44:01:30"),
        ("-:1,2,3", "00:00:00:00:00:00:00:00:00:00:00:00:00:01:02:03"),
        ("01:-", "01:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00"),
        ("01::", "01:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00"),
        ("01", "01:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00"),
        ("01*", "01:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF"),
        ("01:*", "01:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF:FF"),
        ("001122", "00:11:22:00:00:00:00:00:00:00:00:00:00:00:00:00"),
        ("{FFFFFFFF-FFFF-FFFF-0102-03AABB440130}",
         "FF:FF:FF:FF:FF:FF:FF:FF:01:02:03:AA:BB:44:01:30"),
        ("FFFFFFFF-FFFF-FFFF-0102-03AABB440130",
         "FF:FF:FF:FF:FF:FF:FF:FF:01:02:03:AA:BB:44:01:30"),
        ("{FFFFFFFFFFFFFFFE-010203AABB44-0130}",
         "FF:FF:FF:FF:FF:FF:FF:FE:01:02:03:AA:BB:44:01:30"),
    ]
    for shorthand, full in cases:
        assert vscp.guid(shorthand).getAsString() == full, shorthand

def test_invalid_strings():
    for bad in ("01:02:03",                     # too short without fill
                "::" + "FF:" * 16 + "FF",       # too long
                "FF::21::32",                   # two fill placeholders
                "GG:" + "00:" * 14 + "00",      # bad hex
                "010",                          # odd number of hex digits
                "00" * 17):                     # compact form too long
        try:
            vscp.guid(bad)
            assert False, "expected ValueError for " + bad
        except ValueError:
            pass

def test_non_string_non_bytearray_raises():
    try:
        vscp.guid(42)
        assert False, "expected TypeError"
    except TypeError:
        pass


if __name__ == "__main__":
    test_full_colon_form()
    test_lower_case()
    test_grouped_colon_form()
    test_zero_fill_shorthand()
    test_zero_fill_infix()
    test_zero_fill_multibyte_group()
    test_null_guid_shorthands()
    test_dash_colon_zero_fill()
    test_ff_fill_shorthand()
    test_registry_form_with_braces()
    test_registry_form_without_braces()
    test_broadcast_registry_form()
    test_plain_hex_form()
    test_trailing_zero_fill()
    test_trailing_ff_fill()
    test_compact_short_form()
    test_ipv6_style_word_groups()
    test_setFromString()
    test_spec_document_examples()
    test_invalid_strings()
    test_non_string_non_bytearray_raises()
    print("Everything passed")
