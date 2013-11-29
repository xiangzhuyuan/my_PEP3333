# -*- coding: utf-8 -*-

__author__ = 'zhuyuan.xiang'

import os
import re
from shutil import copytree, rmtree
from time import gmtime, strftime
import glob


def _convert_character_to_valid_for_file_name(raw_filename):
    return re.sub(r'[\\/:"*?<>|]+', "_", raw_filename)


def _make_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


if __name__ == '__main__':
    print "hello, world!"
    # read file list from template
    # get current directory
    current_dir = os.path.dirname(os.path.realpath(__file__)) + '/'
    template_file = 'template.md'
    lines = [line.strip() for line in open(current_dir + 'templates/' + template_file)]

    # create file list into pages directory by above file list as filename
    target_directory = current_dir + 'pages/'

    # make a dir

    try:
        if not os.path.exists(target_directory):
            _make_dir(target_directory)
        else:
            rmtree(target_directory)
            _make_dir(target_directory)
    except IOError as e:
        print e
        # create file list
    for line in lines:
        # file name
        try:
            file_name = _convert_character_to_valid_for_file_name(line + '.md')
            f = open(target_directory + file_name, 'wb')
            print "%s -->create successfully" % file_name
            f.close()
        except IOError as e:
            print e
            continue