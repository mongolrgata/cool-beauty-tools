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

    new_ws2_filename = os.path.basename(os.path.splitext(json_filename)[0])

    temp_directory = tempfile.mkdtemp()
    file_names = dearcer.extract('Rio.arc', temp_directory)

    pattern = re.compile(
        b'\x15(\x25\x4c\x43(?P<name>.*?))?\x00\x14(?P<id>..)'
        b'\x00\x00\x63\x68\x61\x72\x00(?P<line>.*?)\x25\x4b\x25\x50\x00',
        re.DOTALL
    )

    for i in range(0, len(file_names)):
        filename = file_names[i]

        if filename == new_ws2_filename:
            with open(os.path.join(temp_directory, filename), 'r+b') as ws2_file:
                content = byteshift.shift_decode(ws2_file.read())

                with open(os.path.abspath(json_filename), 'rt', encoding='utf-8') as json_file:
                    json_object = json.loads(json_file.read())

                for match in pattern.finditer(content):
                    key_id = binascii.hexlify(match.group('id')[::-1]).decode()
                    line = json_object[key_id]['data']['ru']['line'].encode('1251')
                    name = json_object[key_id]['data']['ru']['name'].encode('1251')

                    content = content.replace(
                        match.group(),
                        b''.join([
                            b'\x15',
                            (b'\x25\x4c\x43' + name if name else b''),
                            b'\x00\x14',
                            match.group('id'),
                            b'\x00\x00\x63\x68\x61\x72\x00',
                            line,
                            b'\x25\x4b\x25\x50\x00'
                        ])
                    )

                content = byteshift.shift_encode(content)
                ws2_file.seek(0)
                ws2_file.write(content)
                ws2_file.truncate()

        file_names[i] = os.path.join(temp_directory, filename)

    parcker.pack('Rio.arc', file_names)


def main():
    import_json(sys.argv[1])


if __name__ == '__main__':
    main()
