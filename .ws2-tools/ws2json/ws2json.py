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
        content = f.read()

    content = shift_decode(content)

    pattern = re.compile(
        b'\x15(\x25\x4c\x43(?P<name>.*?))?\x00\x14(?P<id>..)'
        b'\x00\x00\x63\x68\x61\x72\x00(?P<line>.*?)\x25\x4b\x25\x50\x00',
        re.DOTALL
    )

    result = {}

    for match in pattern.finditer(content):
        result[binascii.hexlify(match.group('id')[::-1]).decode()] = {
            'comments': [],
            'data': {
                'en': {
                    'name': (match.group('name') or b'').decode('shift-jis', 'ignore'),
                    'line': (match.group('line') or b'').decode('shift-jis', 'ignore')
                }
            },
            'state': 0
        }

    with open(json_filename, 'wt', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True))


def main():
    convert(sys.argv[1], sys.argv[1] + '.json')


if __name__ == '__main__':
    main()
