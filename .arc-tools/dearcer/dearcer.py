__author__ = 'mongolrgata'

import os
import struct
import sys

NUL_CHAR16 = chr(0).encode('utf-16le')


def read_unsigned_int32(file):
    """
    :param file:
    :type file: io.FileIO
    :return:
    :rtype: int
    """

    return struct.unpack('<L', file.read(4))[0]


def read_filename(file):
    """
    :param file:
    :type file: io.FileIO
    :return:
    :rtype: str
    """

    result = bytearray()

    while True:
        char = file.read(2)

        if char == NUL_CHAR16:
            break

        result.extend(char)

    return result.decode('utf-16le')


def prepare_params(arc_filename):
    """
    :param arc_filename:
    :type arc_filename: str
    :return:
    :rtype (str, str)
    """

    return (
        arc_filename,
        os.path.splitext(arc_filename)[0]
    )


def extract(arc_filename, directory):
    """
    :param arc_filename:
    :type arc_filename: str
    :return:
    :rtype: list[str]
    """

    with open(arc_filename, 'rb') as arc_file:
        file_count = read_unsigned_int32(arc_file)
        arc_file.seek(4, os.SEEK_CUR)  # header_length

        file_lengths = []
        file_names = []

        if not os.path.exists(directory):
            os.mkdir(directory)

        for i in range(0, file_count):
            file_lengths.append(read_unsigned_int32(arc_file))
            arc_file.seek(4, os.SEEK_CUR)  # file_offset
            file_names.append(read_filename(arc_file))

        for i in range(0, file_count):
            with open(os.path.join(directory, file_names[i]), 'wb') as file_out:
                file_out.write(arc_file.read(file_lengths[i]))

    with open(os.path.join(directory, 'order'), 'wt', encoding='utf-8') as order_file:
        order_file.write('\n'.join(file_names))

    return file_names

def main():
    extract(*prepare_params(sys.argv[1]))


if __name__ == '__main__':
    main()
