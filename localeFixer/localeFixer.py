__author__ = 'mongolrgata'

import sys
import os

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

    result = bytearray()

    for char_code in string:
        result.append(rotl8(char_code, 2))

    return bytes(result)


def asciify(string):
    """
    :param string:
    :type string: bytes
    :return:
    :rtype: bytes
    """

    return bytes(string[:1]) * len(string)


def fix(directory):
    """
    :param directory:
    :type directory: str
    :return:
    """

    with open(os.path.join(directory, 'Rio.arc'), 'rb') as rio_file:
        content = rio_file.read()

    for bad_prefix in bad_prefixes:
        jis_prefix = bad_prefix.encode('shift-jis')
        fix_prefix = asciify(jis_prefix)

        content = content.replace(shift_encode(jis_prefix), shift_encode(fix_prefix))

    with open(os.path.join(directory, 'Rio.arc'), 'wb') as rio_file:
        rio_file.write(content)


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
