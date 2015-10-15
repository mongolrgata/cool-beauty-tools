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


def convert(ws2_filename, json_filename, language_code, dummy_mode):
    """
    :param ws2_filename:
    :type ws2_filename: str
    :param json_filename
    :type json_filename: str
    :param language_code
    :type language_code: str
    :param dummy_mode
    :type dummy_mode: bool
    :return:
    """

    with open(ws2_filename, 'rb') as ws2_file:
        content = ws2_file.read()

    content = shift_decode(content)

    pattern = re.compile(
        b'\x15(\x25\x4c\x43(?P<name>.*?))?\x00\x14(?P<id>..)'
        b'\x00\x00\x63\x68\x61\x72\x00(?P<line>.*?)\x25\x4b',
        re.DOTALL
    )

    result = {}

    for match in pattern.finditer(content):
        result[binascii.hexlify(match.group('id')[::-1]).decode()] = {
            'comments': [],
            'data': {
                language_code: {
                    'name': (match.group('name') or b'').decode('shift-jis', 'ignore'),
                    'line': (match.group('line') or b'').decode('shift-jis', 'ignore')
                }
            },
            'state': 0
        } if not dummy_mode else {
            'comments': [],
            'data': {
                language_code: {
                    'name': '',
                    'line': ''
                }
            },
            'state': 0
        }

    with open(json_filename, 'wt', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True))


def main():
    convert(
        sys.argv[1], sys.argv[1] + '.json',
        (sys.argv[2:3] + ['en'])[0],
        (sys.argv[3:4] + [None])[0] == 'dummy-mode'
    )


if __name__ == '__main__':
    main()
