__author__ = 'mongolrgata'

import os
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


def convert(file_in, file_out):
    """
    :param file_in:
    :type file_in: str
    :param file_out
    :type file_out: str
    :return:
    """

    with open(file_in, 'rb') as f:
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
            'line': hex_decode(match[4]),
            'name': hex_decode(match[2])
        })

    with open(file_out, 'w+') as f:
        f.write(json.dumps(result, sort_keys=True, indent=4))


def main():
    file_in = os.path.abspath(sys.argv[1])
    file_out = os.path.splitext(file_in)[0] + '.json'

    convert(file_in, file_out)


if __name__ == '__main__':
    main()
