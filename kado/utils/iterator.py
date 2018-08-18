# kado/utils/iterator.py
# ======================
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


def xlast(iterable):
    """Make an iterator that returns all elements from iterable except the
    last one.


    :param iterable: Iterable to get the elements from.
    :type iterable: ~collections.abc.Iterable


    :returns: An iterator where the last element from iterable is missing.
    :rtype: ~collections.abc.Iterator

    """
    it = iter(iterable)

    try:
        current = next(it)
    except StopIteration:
        return

    while True:
        try:
            follow = next(it)
        except StopIteration:
            break

        yield current
        current = follow
