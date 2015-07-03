__author__ = 'mongolrgata'

import os
import sys
import struct


def read_unsigned_int32(file):
    """
    :param file:
    :type file: io.FileIO
    :return:
    :rtype: int
    """

    return struct.unpack('<L', file.read(4))[0]


def read_char16(file):
    """
    :param file:
    :type file: io.FileIO
    :return:
    :rtype: str
    """

    return chr(struct.unpack('<H', file.read(2))[0])


def read_filename(file):
    """
    :param file:
    :type file: io.FileIO
    :return:
    :rtype: str
    """

    result = ''

    while True:
        char = read_char16(file)

        if char == '\x00':
            break

        result += char

    return result


def extract(arc_filename):
    """
    :param arc_filename:
    :type arc_filename: str
    :return:
    """

    with open(arc_filename, 'rb') as arc_file:
        file_count = read_unsigned_int32(arc_file)
        read_unsigned_int32(arc_file)  # header_length

        file_lengths = []
        file_names = []

        directory = os.path.splitext(arc_filename)[0]
        if not os.path.exists(directory):
            os.mkdir(directory)

        for i in range(0, file_count):
            file_lengths.append(read_unsigned_int32(arc_file))
            read_unsigned_int32(arc_file)  # file_offset
            file_names.append(os.path.join(directory, read_filename(arc_file)))

        for i in range(0, file_count):
            with open(file_names[i], 'wb+') as file_out:
                file_out.write(arc_file.read(file_lengths[i]))


def main():
    extract(sys.argv[1])


if __name__ == '__main__':
    main()
