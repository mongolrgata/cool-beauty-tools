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


def pack(arc_filename, file_names):
    """
    :param arc_filename:
    :type arc_filename: str
    :param file_names:
    :type file_names: list[str]
    :return:
    """

    file_sizes = []
    content = b''

    for filename in file_names:
        file_sizes.append(os.path.getsize(filename))

        with open(filename, 'rb') as file_in:
            content += file_in.read()

    with open(arc_filename, 'wb+') as arc_file:
        file_count = len(file_names)

        write_unsigned_int32(arc_file, file_count)
        write_unsigned_int32(arc_file, 0)  # header_length

        file_offset = 0

        for i in range(0, file_count):
            write_unsigned_int32(arc_file, file_sizes[i])
            write_unsigned_int32(arc_file, file_offset)
            write_filename(arc_file, os.path.basename(file_names[i]))

            file_offset += file_sizes[i]

        header_length = arc_file.tell() - 8

        arc_file.write(content)

        arc_file.seek(4)
        write_unsigned_int32(arc_file, header_length)


def main():
    directory = os.path.abspath(sys.argv[1])
    head, tail = os.path.split(directory)

    pack(
        os.path.join(head, (tail or 'Archive') + '.arc'),
        [f for f in [os.path.join(directory, f) for f in os.listdir(directory)] if os.path.isfile(f)]
    )


if __name__ == '__main__':
    main()
