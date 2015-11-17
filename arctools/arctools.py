__author__ = 'mongolrgata'

import os
import struct
import sys

NUL_CHAR = chr(0).encode('utf-16le')


def read_unsigned_int32(file):
    """
    :param file:
    :type file: io.FileIO
    :return:
    :rtype: int
    """

    return struct.unpack('<L', file.read(4))[0]


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

        if char == NUL_CHAR:
            break

        result.extend(char)

    return result.decode('utf-16le')


def write_filename(file, filename):
    """
    :param file:
    :type file: io.FileIO
    :param filename:
    :type filename: str
    :return:
    :rtype: int
    """

    return file.write(filename.encode('utf-16le') + NUL_CHAR)


def prepare_params_extract(arc_filename):
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


def prepare_params_pack(directory):
    """
    :param directory:
    :type directory: str
    :return:
    :rtype (str, list[str])
    """

    head, tail = os.path.split(directory)

    arc_filename = os.path.join(head, (tail or 'Archive') + '.arc')
    order_filename = os.path.join(directory, 'order')

    if os.path.isfile(order_filename):
        with open(order_filename, 'rt', encoding='utf-8') as order_file:
            file_names = [os.path.join(directory, f) for f in order_file.read().splitlines()]
    else:
        file_names = [f for f in [os.path.join(directory, f) for f in os.listdir(directory)] if os.path.isfile(f)]

    return (
        arc_filename,
        file_names
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


def main():
    if sys.argv[1] == 'extract':
        arc_filename = os.path.abspath(sys.argv[2])
        extract(*prepare_params_extract(arc_filename))
    elif sys.argv[1] == 'pack':
        directory = os.path.abspath(sys.argv[2])
        pack(*prepare_params_pack(directory))


if __name__ == '__main__':
    main()
