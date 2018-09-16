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
import uuid

from contextlib import suppress

from kado import constants as c
from kado.store import mixin
from kado.utils import ghash, htree


__all__ = [
    'Chunk',
    'Index',
    'Item',
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


class Chunk(mixin.HasID, mixin.HasData):
    """Little piece of data composing an item.


    :param data: Data carried by the chunk.
    :type data: python:bytes

    """
    __slots__ = ()


    def __init__(self, data):
        """Constructor for :class:`kado.store.Chunk`."""
        mixin.HasData.__init__(self, data=data)
        mixin.HasID.__init__(self)


    @property
    def data(self):
        """Get stored data."""
        return super().data


    @data.setter
    def data(self, data):
        """Changing the data carried by a chunk is not supported."""
        raise NotImplementedError("chunk cannot be mutated.")


    def _id_get(self):
        """Internal method to get the chunk's unique identifier value.


        :returns: The generated identifier.
        :rtype: ~uuid.UUID

        """
        return uuid.UUID(self.shash[:c.UUID_LEN])


class Item(mixin.HasID, mixin.HasData, mixin.HasMetadata):
    """The primary data structure for kado to store data.


    :param data: The actual data to be stored.
    :type data: python:bytes

    :param metadata: Initial metadata to associate with the item's data.
    :type metadata: python:dict

    """
    __slots__ = ('chunks', )


    def __init__(self, data=b'', metadata=None):
        """Constructor for :class:`kado.store.Item`."""
        self.chunks = []

        mixin.HasMetadata.__init__(self, metadata)
        mixin.HasData.__init__(self, data=data)
        mixin.HasID.__init__(self)


    def __len__(self):
        """Return the bytes length of the item."""
        return sum(len(chunk) for chunk in self.chunks)


    @staticmethod
    def _shash_init(size=c.BLAKE2_DATA_LENGTH, seed=c.BLAKE2_DATA_SEED):
        """Initialize the object to compute a strong cryptographic hash of
        stored data.


        :param size: Length of the digest size to be returned by the hash
                     function.
        :type size: python:int

        :param seed: Random string to randomize the output of the hash function.
        :type seed: python:bytes


        :returns: The initialized cryptographic hash function.

        """
        return htree.HTree(mixin.HasData._shash_init(size, seed))


    @staticmethod
    def _whash_init(seed=c.XXH64_DATA_SEED):
        """Initialize the object to compute a weak hash of stored data.


        :param seed: Random string to randomize the output of the hash function.
        :type seed: python:bytes


        :returns: The initialized hash function.

        """
        return htree.HTree(mixin.HasData._whash_init(seed=seed))


    def _data_hash(self, h):
        """Update given hash object with the object's data.


        :param h: The hash function to be updated.

        """
        for chunk in self.chunks:
            h.update(chunk.data)


    def _data_get(self):
        """Return item's stored data.


        :returns: The data carried by the object.
        :rtype: python:bytes

        """
        return b''.join(x.data for x in self.chunks)


    def _data_set(self, data):
        """Set given data into the item.


        :param data: Data to be stored by the object.
        :type data: python:bytes


        :raises TypeError: When given data is not a bytes-like object.

        """
        if not isinstance(data, bytes):
            raise TypeError('expected {}, got {}.'.format(bytes, type(data)))
        self.chunks = [Chunk(chunk) for _, _, chunk in ghash.chop(data)]


    def copy(self):
        """Return a copy (“clone”) of the item.


        :returns: A copy of the item.
        :rtype: ~kado.store._store.Item

        """
        obj = Item(metadata={k: v for k, v in self.items()})
        obj.chunks = self.chunks.copy()

        return obj
