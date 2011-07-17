#!/usr/bin/env python

import sys

from argparse import ArgumentParser
from webjet import WebProject

def main(argv):
    parser = ArgumentParser(description='Generate static webprojects')

    # Add arguments ...
    parser.add_argument('cfg_files', type=str, nargs='+')
    parser.add_argument('-I', '--include', action='append', dest='includes')

    options = parser.parse_args()

    for inc in (options.includes or []):
        if inc not in sys.path:
            sys.path.append(inc)

    for cfg_file in options.cfg_files:
        print('Creating Project with config file:', cfg_file)
        webproject = WebProject(cfg_file)

        webproject.load_modules()

main(sys.argv)
