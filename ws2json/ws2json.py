__author__ = 'mongolrgata'

import binascii
import json
import re
import sys


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

    return bytes([rotr8(char_code, 2) for char_code in string])


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
            'name': shift_decode(match.group('name') or '').decode('shift-jis', 'ignore'),
            'id': binascii.hexlify(match.group('id')).decode(),
            'line': {
                'en': shift_decode(match.group('line')).decode('shift-jis', 'ignore')
            }
        })

    with open(json_filename, 'wt', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True))


def main():
    convert(sys.argv[1], sys.argv[1] + '.json')


if __name__ == '__main__':
    main()
