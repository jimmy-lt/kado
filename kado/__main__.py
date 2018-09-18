# kado/__main__.py
# ================
#
# Copying
# -------
#
# Copyright (c) 2018 kado authors.
#
# This file is part of the *kado* project.
#
# kado is a free software project. You can redistribute it and/or
# modify if under the terms of the MIT License.
#
# This software project is distributed *as is*, WITHOUT WARRANTY OF ANY
# KIND; including but not limited to the WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE and NONINFRINGEMENT.
#
# You should have received a copy of the MIT License along with kado.
# If not, see <http://opensource.org/licenses/MIT>.
#
import sys
import logging
import argparse

from kado import __version__


log = logging.getLogger(__name__)


#: Name of the kado program.
PROG_NAME = 'kado'
#: Short description text for the kado program.
PROG_DESCRIPTION = 'An object storage manager.'


def parse_args(args):
    parser = argparse.ArgumentParser(prog=PROG_NAME,
                                     description=PROG_DESCRIPTION)

    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s {version}'.format(version=__version__))

    return vars(parser.parse_args(args))


def main():
    opts = parse_args(sys.argv[1:])


if __name__ == '__main__':
    main()
