__author__ = 'mongolrgata'

import sys
import re
import binascii
import json


def hex_decode(original):
    """
    :param original:
    :return:
    """

    return binascii.hexlify(original).decode()


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

    matches = re.findall(
        b'(\x54(\x94\x31\x0D(.*?))?\x00\x50(..)\x00\x00\x8D\xA1\x85\xC9\x00(.*?)\x94\x2D\x94\x41\x00)',
        text,
        re.DOTALL
    )

    result = []

    for match in matches:
        result.append({
            'id': hex_decode(match[3]),
            'name': hex_decode(match[2]),
            'line': {
                'en': hex_decode(match[4]),
                'ru': '',
                'state': None
            }
        })

    with open(json_filename, 'w+') as f:
        f.write(json.dumps(result, sort_keys=True, indent=4))


def main():
    convert(sys.argv[1], sys.argv[1] + '.json')


if __name__ == '__main__':
    main()
