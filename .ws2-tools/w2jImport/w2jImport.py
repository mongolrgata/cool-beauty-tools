__author__ = 'mongolrgata'

import binascii
import json
import os
import re
import sys
import tempfile

import byteshift
import dearcer
import parcker


def import_json(json_filename):
    """
    :param json_filename:
    :type json_filename: str
    :return:
    """

    with open(json_filename, 'rt', encoding='utf-8') as json_file:
        json_object = json.loads(json_file.read())

    temp_directory = tempfile.mkdtemp()
    file_names = dearcer.extract('Rio.arc', temp_directory)

    ws2_filename = os.path.splitext(os.path.basename(json_filename))[0]

    with open(os.path.join(temp_directory, ws2_filename), 'r+b') as ws2_file:
        content = byteshift.shift_decode(ws2_file.read())

        pattern = re.compile(
            b'\x15(\x25\x4c\x43(?P<name>.*?))?\x00\x14(?P<id>..)'
            b'\x00\x00\x63\x68\x61\x72\x00(?P<line>.*?)\x25\x4b\x25\x50\x00',
            re.DOTALL
        )

        for match in pattern.finditer(content):
            encode_id = match.group('id')
            decode_id = binascii.hexlify(encode_id[::-1]).decode()

            line = json_object[decode_id]['data']['ru']['line'].encode('1251')
            name = json_object[decode_id]['data']['ru']['name'].encode('1251')

            content = content.replace(
                match.group(),
                b''.join([
                    b'\x15',
                    (b'\x25\x4c\x43' + name if name else b''),
                    b'\x00\x14',
                    encode_id,
                    b'\x00\x00\x63\x68\x61\x72\x00',
                    line,
                    b'\x25\x4b\x25\x50\x00'
                ])
            )

        content = byteshift.shift_encode(content)

        ws2_file.seek(0)
        ws2_file.write(content)
        ws2_file.truncate()

    parcker.pack('Rio.arc', [os.path.join(temp_directory, file_name) for file_name in file_names])


def main():
    import_json(sys.argv[1])


if __name__ == '__main__':
    main()
