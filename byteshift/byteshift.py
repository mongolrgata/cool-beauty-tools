__author__ = 'mongolrgata'

import sys


def rotr8(int8, shift_size):
    """
    :param int8:
    :type int8: int
    :param shift_size:
    :type shift_size: int
    :return:
    :rtype: int
    """

    return (int8 >> shift_size) | (int8 << (8 - shift_size) & 0xff)


def shift_decode(string):
    """
    :param string:
    :type string: bytes
    :return:
    :rtype: bytes
    """

    return bytes([rotr8(char_code, 2) for char_code in string])


def rotl8(int8, shift_size):
    """
    :param int8:
    :type int8: int
    :param shift_size:
    :type shift_size: int
    :return:
    :rtype: int
    """

    return (int8 << shift_size) & 0xff | (int8 >> (8 - shift_size))


def shift_encode(string):
    """
    :param string:
    :type string: bytes
    :return:
    :rtype: bytes
    """

    return bytes([rotl8(char_code, 2) for char_code in string])


def shift(direction, filename):
    with open(filename, 'r+b') as ws2_file:
        content = ws2_file.read()

        if direction == 'right':
            content = shift_decode(content)
        elif direction == 'left':
            content = shift_encode(content)

        ws2_file.seek(0)
        ws2_file.write(content)
        ws2_file.truncate()


def main():
    shift(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
