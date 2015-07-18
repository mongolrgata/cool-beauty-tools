__author__ = 'mongolrgata'

import os
import struct
import sys

NUL_CHAR16 = chr(0).encode('utf-16le')


def write_unsigned_int32(file, value):
    """
    :param file:
    :type file: io.FileIO
    :param value:
    :type value: int
    :return:
    :rtype: int
    """

    return file.write(struct.pack('<L', value))


def write_filename(file, filename):
    """
    :param file:
    :type file: io.FileIO
    :param filename:
    :type filename: str
    :return:
    :rtype: int
    """

    return file.write(filename.encode('utf-16le') + NUL_CHAR16)


def pack(arc_filename, file_names):
    """
    :param arc_filename:
    :type arc_filename: str
    :param file_names:
    :type file_names: list[str]
    :return:
    """

    with open(arc_filename, 'wb') as arc_file:
        file_count = len(file_names)

        write_unsigned_int32(arc_file, file_count)
        write_unsigned_int32(arc_file, 0)  # header_length

        file_offset = 0

        for i in range(0, file_count):
            file_size = os.path.getsize(file_names[i])

            write_unsigned_int32(arc_file, file_size)
            write_unsigned_int32(arc_file, file_offset)
            write_filename(arc_file, os.path.basename(file_names[i]))

            file_offset += file_size

        header_length = arc_file.tell() - 8

        for filename in file_names:
            with open(filename, 'rb') as file_in:
                arc_file.write(file_in.read())

        arc_file.seek(4)
        write_unsigned_int32(arc_file, header_length)


def prepare_params(directory):
    """
    :param directory:
    :type directory: str
    :return:
    :rtype (str, list[str])
    """

    directory = os.path.abspath(directory)
    head, tail = os.path.split(directory)

    arc_filename = os.path.join(head, (tail or 'Archive') + '.arc')
    order_filename = os.path.join(directory, 'order')

    if os.path.isfile(order_filename):
        with open(order_filename, 'rt', encoding='utf-8') as order_file:
            file_names = [os.path.join(directory, f) for f in order_file.read().splitlines()]
    else:
        file_names = [f for f in [os.path.join(directory, f) for f in os.listdir(directory)] if os.path.isfile(f)]

    return arc_filename, file_names


def main():
    pack(*prepare_params(sys.argv[1]))


if __name__ == '__main__':
    main()
