__author__ = 'mongolrgata'

import os
import sys
import struct


def write_unsigned_int32(file, value):
    """
    :param file:
    :type file: io.FileIO
    :param value:
    :type value: int
    :return:
    """

    return file.write(struct.pack('<L', value))


def write_filename(file, filename):
    """
    :param file:
    :type file: io.FileIO
    :param filename:
    :type filename: str
    :return:
    """

    for char in filename:
        file.write(char.encode() + b'\x00')

    return file.write(b'\x00\x00')


def main():
    file_names = []
    file_sizes = []
    content = b''

    for filename in sys.argv[2:]:
        file_names.append(os.path.basename(filename))
        file_sizes.append(os.path.getsize(filename))

        with open(filename, 'rb') as file_in:
            content += file_in.read()

    with open(sys.argv[1], 'wb+') as arc_file:
        file_count = len(sys.argv) - 2

        write_unsigned_int32(arc_file, file_count)
        write_unsigned_int32(arc_file, 0)

        file_offset = 0

        for i in range(0, file_count):
            write_unsigned_int32(arc_file, file_sizes[i])
            write_unsigned_int32(arc_file, file_offset)
            write_filename(arc_file, file_names[i])

            file_offset += file_sizes[i]

        header_length = arc_file.tell() - 2

        arc_file.write(content)

        arc_file.seek(4)
        write_unsigned_int32(arc_file, header_length)


if __name__ == '__main__':
    main()
