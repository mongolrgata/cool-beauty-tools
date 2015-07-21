__author__ = 'mongolrgata'

import json
import os
import sys


def dict_merge(dict1, dict2):
    """
    :param dict1:
    :type dict1: dict
    :param dict2:
    :type dict2: dict
    :return:
    """

    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                dict_merge(dict1[key], dict2[key])
                continue

        dict1[key] = dict2[key]


def merge(directory_list):
    """
    :param directory_list:
    :type directory_list: list[str]
    :return:
    """

    sets = []

    for directory in directory_list:
        sets.append(set([f for f in os.listdir(directory)]))

    file_names = set.intersection(*sets)

    for filename in file_names:
        result = {}

        for directory in directory_list:
            with open(os.path.join(directory, filename), 'rt', encoding='utf-8') as json_file_in:
                content = json_file_in.read()
                json_object = json.loads(content)

            dict_merge(result, json_object)

        with open(filename, 'wt', encoding='utf-8') as json_file_out:
            json_file_out.write(json.dumps(result, ensure_ascii=False, indent=4, sort_keys=True))


def main():
    merge(sys.argv[1:])


if __name__ == '__main__':
    main()
