# kado/store/mixin.py
# ===================
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

import hmac
import xxhash
import hashlib

from kado import constants as c


class HasID(object):
    """Store mixin to provide a unique identifier."""

    def __init__(self):
        """Constructor for :class:`kado.store.mixin.HasID`."""
        self._id = self._id_get()


    @staticmethod
    def _id_get():
        """Internal method to get the identifier value. This method is meant to
        be overridden by subclasses in order to generate their own identifier.


        :returns: The generated identifier.
        :rtype: ~typing.Any

        """
        return uuid.uuid4()


    @property
    def id(self):
        """Get the object's unique identifier.


        :returns: The object's unique identifier.
        :rtype: ~typing.Any

        """
        return self._id


class HasData(object):
    """Mixin class to cary binary data.


    :param data: Data to be carried.
    :type data: python:bytes

    """

    def __init__(self, data=b''):
        """Constructor for :class:`kado.store.mixin.HasData`."""
        self._shash = None    # Strong hash handler.
        self._whash = None    # Weak hash handler.
        # Flags to track hash state compared to stored data.
        self._shash_dirty = self._whash_dirty = False

        self._data = None
        self._data_set(data)


    def __eq__(self, other):
        """Securely compare this data container with another.


        :param other: The other object to compare with.
        :type other: ~kado.store.mixin.HasData | python:bytes


        :returns: Whether both data containers are equal or not.
        :rtype: python:bool


        :raises TypeError: When other is not a bytes-like object.

        """
        try:
            return hmac.compare_digest(self.data, other.data)
        except AttributeError:
            return hmac.compare_digest(self.data, other)


    def __hash__(self):
        """Return the hash value of the object.


        :returns: The integer hash value of the object.
        :rtype: python:int

        """
        return hash(self.data)


    def __len__(self):
        """Return length of stored data.


        :returns: Length of the stored data.
        :rtype: python:int

        """
        return len(self.data)


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
        return hashlib.blake2b(digest_size=size, person=seed)


    @staticmethod
    def _whash_init(seed=c.XXH64_DATA_SEED):
        """Initialize the object to compute a weak hash of stored data.


        :param seed: Random string to randomize the output of the hash function.
        :type seed: python:bytes


        :returns: The initialized hash function.

        """
        return xxhash.xxh64(seed=seed)


    @property
    def data(self):
        """Get stored data."""
        return self._data_get()


    @data.setter
    def data(self, data):
        """Set data to be stored.


        :param data: The data to be stored.
        :type data: python:bytes

        """
        self._data_set(data)
        self._shash_dirty = self._whash_dirty = True


    @property
    def shash(self):
        """Compute a strong cryptographic hash of the stored data.


        :returns: Hexadecimal digest of the hashed data.
        :rtype: python:str

        """
        if self._shash_dirty or self._shash is None:
            self._shash = self._shash_init()

            self._data_hash(self._shash)
            self._shash_dirty = False

        return self._shash.hexdigest()


    @property
    def whash(self):
        """Compute a weak hash of the stored data.


        :returns: Hexadecimal digest of the hashed data.
        :rtype: python:str

        """
        if self._whash_dirty or self._whash is None:
            self._whash = self._whash_init()

            self._data_hash(self._whash)
            self._whash_dirty = False

        return self._whash.hexdigest()


    def _data_hash(self, h):
        """Update given hash object with the object's data.


        :param h: The hash function to be updated.

        """
        h.update(self.data)


    def _data_get(self):
        """Return object's stored data.


        :returns: The data carried by the object.
        :rtype: python:bytes

        """
        return self._data


    def _data_set(self, data):
        """Set given data into the object.


        :param data: Data to be stored by the object.
        :type data: python:bytes


        :raises TypeError: When given data is not a bytes-like object.

        """
        if not isinstance(data, bytes):
            raise TypeError('expected {}, got {}.'.format(bytes, type(data)))
        self._data = data
