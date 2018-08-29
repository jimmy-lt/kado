# kado/store/_store.py
# ====================
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
from contextlib import suppress


__all__ = [
    'Index',
]


class Index(object):
    """Store associative data structure in which a key can map to one or
    multiple values.

    """
    __slots__ = ('_mapping', )


    def __init__(self):
        """Constructor for :class:`kado.store.Index`."""
        self._mapping = {}


    def __contains__(self, key):
        """Check if given key is present in the index.


        :param key: Registered index key.
        :type key: ~collections.abc.Hashable


        :returns: Whether given key is defined in the index.
        :rtype: python:bool

        """
        return key in self._mapping


    def __len__(self):
        """Return the number of entries within the index.


        :returns: Number of entries stored in the index.
        :rtype: python:int

        """
        return len(self._mapping)


    def __iter__(self):
        """Return and iterator over the stored index keys.


        :returns: An iterator over the index key.
        :rtype: ~collections.abc.Iterator

        """
        return iter(self._mapping)


    def clear(self):
        """Remove all entries from the index or if a key is specified, remove
        all entries registered with given key.


        :param key: Key mapping to the entries to remove from the index.
        :type key: ~collections.abc.Hashable

        """
        self._mapping.clear()


    def count(self, key=None):
        """Get the number of entries registered with the index if a key is
        specified, get the number of entries registered with this specific key.


        :param key: Key mapping to the index entries.
        :type key: ~collections.abc.Hashable


        :returns: Number of entries registered within the index.
        :rtype: python:int


        :raises KeyError: When the key cannot be found in the index.

        """
        if key is None:
            return sum(len(x) for x in self._mapping.values())
        else:
            return len(self._mapping[key])


    def get(self, key):
        """Retrieve the entries registered under given key from the index.


        :param key: Key mapping to the index entries.
        :type key: ~collections.abc.Hashable


        :returns: The entries matching given key.
        :rtype: ~collections.abc.MutableSequence


        :raises KeyError: When the key cannot be found in the index.

        """
        return [x for x in self._mapping[key]]


    def add(self, key, value):
        """Add an entry to the index.


        :param key: Key to find back the entry in the index.
        :type key: ~collections.abc.Hashable

        :param value: Value of the index entry.
        :type value: ~collections.abc.Hashable

        """
        self._mapping.setdefault(key, set()).add(value)


    def remove(self, key, value=None):
        """Remove an entry from the index.


        :param key: Key to the entry to be removed from the index.
        :type key: ~collections.abc.Hashable

        :param value: Value of the entry.
        :type value: ~collections.abc.Hashable


        :raises KeyError: When the key cannot be found in the index.

        :raises ValueError: When given value is not registered under given key.

        """
        if value is None:
            del self._mapping[key]
        else:
            st = self._mapping[key]
            try:
                st.remove(value)
            except KeyError:
                raise ValueError(key, value)

            if not len(st):
                del self._mapping[key]


    def discard(self, key, value=None):
        """Remove an entry from the index if present.


        :param key: Key to the entry to be removed from the index.
        :type key: ~collections.abc.Hashable

        :param value: Value of the entry.
        :type value: ~collections.abc.Hashable

        """
        with suppress(KeyError, ValueError):
            self.remove(key, value)
