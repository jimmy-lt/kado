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
import pkg_resources

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

    pkg_actions = {
        e.name: (e.load()(), str(e).split('=')[1].strip())
        for e in pkg_resources.iter_entry_points('kado.actions')
    }

    if pkg_actions:
        action_p = parser.add_subparsers(title='action',
                                         dest='action',
                                         metavar='<action>')

        seen = set()
        for action, dist in pkg_actions.values():
            if seen.intersection(action.names):
                # We cannot accept two actions carrying the same name.
                log.debug("Action names collision for {} on {}".format(
                    dist, seen.intersection(action.names)
                ))
                continue

            log.debug("Parsing arguments for action {}.".format(dist))
            curr_p = action_p.add_parser(action.names[0],
                                         aliases=action.names[1:],
                                         help=action.description)

            for a_args, a_kwargs in action.arguments:
                curr_p.add_argument(*a_args, **a_kwargs)

            seen.update(action.names)

    return vars(parser.parse_args(args))


def main():
    opts = parse_args(sys.argv[1:])


if __name__ == '__main__':
    main()
