__author__ = 'mongolrgata'

import sys
import re
import binascii
import json


def rotr8(int8, shift):
    """
    :param int8:
    :type int8: int
    :param shift:
    :type shift: int
    :return:
    :rtype: int
    """

    return (int8 >> shift) | (int8 << (8 - shift) & 0xff)


def shift_decode(string):
    """
    :param string:
    :type string: bytes
    :return:
    :rtype: bytes
    """

    result = bytearray()

    for char_code in string:
        result.append(rotr8(char_code, 2))

    return bytes(result)


def hex_decode(string):
    """
    :param string:
    :return:
    :rtype: str
    """

    return binascii.hexlify(string).decode()


def convert(ws2_filename, json_filename):
    """
    :param ws2_filename:
    :type ws2_filename: str
    :param json_filename
    :type json_filename: str
    :return:
    """

    with open(ws2_filename, 'rb') as f:
        text = f.read()

    pattern = re.compile(
        b'\x54(\x94\x31\x0D(?P<name>.*?))?\x00\x50(?P<id>..)'
        b'\x00\x00\x8D\xA1\x85\xC9\x00(?P<line>.*?)\x94\x2D\x94\x41\x00',
        re.DOTALL
    )

    result = []

    for match in pattern.finditer(text):
        result.append({
            'name': shift_decode(match.group('name') or '').decode(),
            'id': hex_decode(match.group('id')),
            'line': {
                'en': shift_decode(match.group('line')).decode()
            }
        })

    with open(json_filename, 'w+') as f:
        f.write(json.dumps(result, sort_keys=True, indent=4))


def main():
    convert(sys.argv[1], sys.argv[1] + '.json')


if __name__ == '__main__':
    main()
