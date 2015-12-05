import os
import struct
import sys
import tempfile

__author__ = 'mongolrgata'
NUL_CHAR = chr(0).encode('utf-16le')


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


def shift_decode(string):
    """
    :param string:
    :type string: bytes
    :return:
    :rtype: bytes
    """

    return bytes([rotr8(char_code, 2) for char_code in string])


def shift_encode(string):
    """
    :param string:
    :type string: bytes
    :return:
    :rtype: bytes
    """

    return bytes([rotl8(char_code, 2) for char_code in string])


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

        if char == NUL_CHAR:
            break

        result.extend(char)

    return result.decode('utf-16le')


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

    return file.write(filename.encode('utf-16le') + NUL_CHAR)


def prepare_params_extract():
    """
    :return:
    :rtype (str, str)
    """

    arc_filename = os.path.abspath(sys.argv[2])

    return (
        arc_filename,
        os.path.splitext(arc_filename)[0]
    )


def prepare_params_pack():
    """
    :return:
    :rtype (str, list[str])
    """

    directory = os.path.abspath(sys.argv[2])
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


def prepare_params_fix():
    """
    :return:
    :rtype (str, )
    """

    return (
        os.path.abspath(os.getcwd()),
    )


def extract(arc_filename, directory):
    """
    :param arc_filename:
    :type arc_filename: str
    :param directory:
    :type directory: str
    :return:
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


def fix(directory):
    """
    :param directory:
    :type directory: str
    :return:
    """

    bad_prefixes = [
        'A小鳥',
        'Bあげは',
        'C天音',
        'D亜紗',
        'E夜瑠',
        'Fひばり',
        'Gほたる',
        'H朱莉',
        'I佳奈子',
        'J達也',
        'K柾次',
        'L鯨',
        'M碧',
        'Nイスカ',
        'O早苗',
        'P亮子',
        'Q由佳',
        'Rハット',
        'S隆夫'
    ]

    rio_filename = os.path.join(directory, 'Rio.arc')
    graphic_filename = os.path.join(directory, 'Graphic.arc')

    rio_dict = {}
    graphic_dict = {}

    for bad_prefix in bad_prefixes:
        jis_prefix = bad_prefix.encode('shift-jis')
        fix_prefix = bytes(jis_prefix[:1]) * len(jis_prefix)

        rio_dict[shift_encode(jis_prefix)] = shift_encode(fix_prefix)
        graphic_dict[bad_prefix] = fix_prefix.decode()
    ####################################################################################################################
    with open(rio_filename, 'r+b') as rio_file:
        content = rio_file.read()

        for bad_prefix, fix_prefix in rio_dict.items():
            content = content.replace(bad_prefix, fix_prefix)

        rio_file.seek(0)
        rio_file.write(content)
        rio_file.truncate()
    ####################################################################################################################
    temp_directory = tempfile.mkdtemp()
    extract(graphic_filename, temp_directory)

    order_filename = os.path.join(temp_directory, 'order')
    with open(order_filename, 'rt', encoding='utf-8') as order_file:
        file_names = order_file.read().splitlines()

    for i in range(0, len(file_names)):
        filename = file_names[i]

        for bad_prefix, fix_prefix in graphic_dict.items():
            if filename.startswith(bad_prefix):
                fix_filename = os.path.join(temp_directory, fix_prefix + filename[len(bad_prefix):])
                os.replace(os.path.join(temp_directory, filename), fix_filename)
                file_names[i] = fix_filename

                break
        else:
            file_names[i] = os.path.join(temp_directory, filename)

    pack(graphic_filename, file_names)


def main():
    if sys.argv[1] == 'extract':
        extract(*prepare_params_extract())
    elif sys.argv[1] == 'pack':
        pack(*prepare_params_pack())
    elif sys.argv[1] == 'fix':
        fix(*prepare_params_fix())


if __name__ == '__main__':
    main()
