import os
import struct
import sys

__author__ = 'mongolrgata'


def read_unsigned_int32(file):
    """
    :param file:
    :type file: io.FileIO
    :return:
    :rtype: int
    """

    return struct.unpack('<L', file.read(4))[0]


def extract(pna_filename):
    """
    :param pna_filename:
    :type pna_filename: str
    :return:
    """

    with open(pna_filename, 'rb') as pna_file:
        pna_file.seek(16, os.SEEK_CUR)
        file_count = read_unsigned_int32(pna_file)

        file_names = []
        file_lengths = []

        directory = os.path.splitext(pna_filename)[0]
        if not os.path.exists(directory):
            os.mkdir(directory)

        for i in range(0, file_count):
            pna_file.seek(4, os.SEEK_CUR)
            file_names.append(os.path.join(directory, str(read_unsigned_int32(pna_file)).zfill(3) + '.png'))
            pna_file.seek(28, os.SEEK_CUR)
            file_lengths.append(read_unsigned_int32(pna_file))

        for i in range(0, file_count):
            if not file_lengths[i]:
                continue

            with open(file_names[i], 'wb') as file_out:
                file_out.write(pna_file.read(file_lengths[i]))


def main():
    pna_filename = os.path.abspath(sys.argv[1])
    extract(pna_filename)


if __name__ == '__main__':
    main()
