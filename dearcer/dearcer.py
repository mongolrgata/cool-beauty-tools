__author__ = 'mongolrgata'

import os
import sys

script_directory = os.path.dirname(os.path.abspath(__file__))


def read_unsigned_int32(file):
    return int.from_bytes(file.read(4), byteorder='little')


def read_char16(file):
    return chr(file.read(2)[0])


def extract(arc_file_name):
    with open(arc_file_name, 'rb') as arc_file:
        file_count = read_unsigned_int32(arc_file)
        read_unsigned_int32(arc_file)  # header length

        file_lengths = []
        file_names = []

        for i in range(0, file_count):
            file_lengths.append(read_unsigned_int32(arc_file))
            read_unsigned_int32(arc_file)  # file offset

            file_names.append('')

            while True:
                char = read_char16(arc_file)

                if ord(char) == 0:
                    break

                file_names[i] += char

        directory = script_directory + '\\' + os.path.splitext(os.path.basename(arc_file_name))[0]

        if not os.path.exists(directory):
            os.mkdir(directory)

        for i in range(0, file_count):
            with open(directory + '\\' + file_names[i], 'wb+') as file_out:
                file_out.write(arc_file.read(file_lengths[i]))


def main():
    for filename in sys.argv[1:]:
        extract(filename)


if __name__ == '__main__':
    main()
