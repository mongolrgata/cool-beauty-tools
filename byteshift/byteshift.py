__author__ = 'mongolrgata'

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

    result = bytearray()

    for char_code in string:
        result.append(rotr8(char_code, 2))

    return bytes(result)


def rotl8(int8, shift):
    """
    :param int8:
    :type int8: int
    :param shift:
    :type shift: int
    :return:
    :rtype: int
    """

    return (int8 << shift) & 0xff | (int8 >> (8 - shift))


def shift_encode(string):
    """
    :param string:
    :type string: bytes
    :return:
    :rtype: bytes
    """

    result = bytearray()

    for char_code in string:
        result.append(rotl8(char_code, 2))

    return bytes(result)


def shift(direction, filename):
    with open(filename, 'rb') as ws2_file:
        content = ws2_file.read()

    if direction == 'right':
        content = shift_decode(content)
        filename += '.right'
    elif direction == 'left':
        content = shift_encode(content)
        filename += '.left'

    with open(filename, 'wb') as ws2_file:
        ws2_file.write(content)


def main():
    shift(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
