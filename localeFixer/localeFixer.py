__author__ = 'mongolrgata'

import os
import sys
import tempfile

import dearcer
import parcker

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


def rotl8(int8, shift):
    """
    :param int8:
    :type int8: int
    :param shift:
    :type shift: int
    :return:
    :rtype: int
    """

    return (int8 << shift) & 0xff | (int8 >> (8 - shift))


def shift_encode(string):
    """
    :param string:
    :type string: bytes
    :return:
    :rtype: bytes
    """

    return bytes([rotl8(char_code, 2) for char_code in string])


def fix(directory):
    """
    :param directory:
    :type directory: str
    :return:
    """

    ####################################################################################################################
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

    file_names = dearcer.extract(graphic_filename, temp_directory)

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

    parcker.pack(graphic_filename, file_names)
    ####################################################################################################################


def prepare_params(directory):
    """
    :param directory:
    :type directory: str
    :return:
    :rtype (str, )
    """

    return tuple([directory])


def main():
    fix(*prepare_params((sys.argv[1:2] + [''])[0]))


if __name__ == '__main__':
    main()
