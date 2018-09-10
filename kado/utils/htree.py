# kado/utils/htree.py
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
import hashlib

from itertools import zip_longest
from collections import deque


class HTree(object):
    """A binary tree in which every leaf node is labelled with the cryptographic
    hash of a given data block and every non-leaf node is labelled with the
    cryptographic hash of the labels of its child nodes.


    ..code-block:

                          ---------------
                         |     Root      |
                         |---------------|
                         | hash(n0 + n1) |
                          ---------------
                         /               \
             ---------------           ---------------
            |    Node 0     |         |    Node 1     |
            |---------------|         |---------------|
            | hash(n2 + n3) |         | hash(n4 + n5) |
             ---------------           ---------------
              /           \             /           \
         ----------   ----------   ----------   ----------
        |  Node 2  | |  Node 3  | |  Node 4  | |  Node 5  |
        |----------| |----------| |----------| |----------|
        | hash(d0) | | hash(d1) | | hash(d2) | | hash(d3) |
         ----------   ----------   ----------   ----------
              |            |            |            |
         -------------------------------------------------
        |    d0           d1           d2           d3    |
         -------------------------------------------------
                            data blocks


    The tree is managed as a sequence where leaves are added or removed and
    therefore supports a subset of the :class:`~collections.abc.MutableSequence`
    operations.

    The tree also acts as a conventional :mod:`hashlib` object.


    :param hash: Hash function to use.
    :type hash: python:str | ~collection.abc.Callable

    :param iterable: An iterable with the data to initialize the tree with.
    :type iterable: ~collections.abc.Iterable

    """
    __slots__ = ('_hash', '_leaves')


    def __init__(self, hash, iterable=None):
        """Constructor for :class:`kado.utils.htree.Htree`."""
        self._leaves = deque()

        # Generate hash object to reuse it when needed.
        if isinstance(hash, str):
            self._hash = hashlib.new(hash)
        else:
            try:
                self._hash = hash()
            except TypeError:
                self._hash = hash

        if iterable is not None:
            self.extend(iterable)


    def __iter__(self):
        """Return an iterator over the digest of the data passed to the tree's
        leaf. Theses are bytes objects of size
        :meth:`~kado.utils.htree.Htree.digest_size` which may contain bytes in
        the whole range from 0 to 255.


        :returns: An iterator over the leaf hash bytes.
        :rtype: ~collections.abc.Iterator

        """
        return iter(self._leaves)


    def __len__(self):
        """Get the number of leaves stored in the hash tree.


        :returns: Number of leaves stored in the hash tree.
        :rtype: python:int

        """
        return len(self._leaves)


    def __delitem__(self, i):
        """Remove a leaf from the tree.


        :param i: Index of the leaf to be removed.
        :type i: python:int


        :raises IndexError: When given index is out of range.

        """
        del self._leaves[i]


    def __getitem__(self, i):
        """Get the digest of the data passed to the tree's leaf at given index.
        This is a bytes object of size
        :meth:`~kado.utils.htree.Htree.digest_size` which may contain bytes in
        the whole range from 0 to 255.


        :param i: Index of the requested leaf digest.
        :type i: python:int


        :returns: The leaf hash bytes.
        :rtype: python:bytes


        :raises IndexError: When given index is out of range.

        """
        return self._leaves[i]


    def __setitem__(self, i, data):
        """Set a leaf in the tree.


        :param i: Index at which the leaf must be set.
        :type i: python:int

        :param data: The actual leaf data to be hashed.
        :type data: python:bytes


        :raises IndexError: When given index is out of range.

        :raises TypeError: When given data does not support the buffer protocol.

        """
        self._leaves[i] = self._data_digest(data)


    @property
    def block_size(self):
        """The internal block size of the hash algorithm in bytes."""
        return self._hash.block_size


    @property
    def digest_size(self):
        """The size of the resulting hash in bytes."""
        return self._hash.digest_size


    @property
    def name(self):
        """The canonical name of this hash, always lowercase."""
        return self._hash.name


    def _data_digest(self, data):
        """Digest given data using the tree's hash object.


        :param data: The data to be digested.
        :type data: python:bytes


        :returns: A bytes digest of the data of size
                  :meth:`~kado.utils.htree.Htree.digest_size` which may contain
                  bytes in the whole range from 0 to 255.
        :rtype: python:bytes


        :raises TypeError: When given data does not support the buffer protocol.

        """
        hash = self._hash.copy()
        hash.update(data)

        return hash.digest()


    def copy(self):
        """Return a copy (“clone”) of the hash tree object. This can be used to
        efficiently compute the digests of data sharing a common initial
        leaves.


        :returns: A copy of the hash tree object.
        :rtype: ~kado.utils.htree.Htree

        """
        h = HTree(hash=self._hash.copy())
        h._leaves = self._leaves.copy()

        return h


    def digest(self, i=None):
        """Return the digest of the data passed to the
        :meth:`~kado.utils.htree.Htree.update` method so far. This is a bytes
        object of size :meth:`~kado.utils.htree.Htree.digest_size` which may
        contain bytes in the whole range from 0 to 255.


        :param i: If given, returns the digest of the data for the leaf at this
                  index.
        :type i: python:int


        :returns: A bytes digest of the data of size
                  :meth:`~kado.utils.htree.Htree.digest_size` which may contain
                  bytes in the whole range from 0 to 255.
        :rtype: python:bytes


        :raises IndexError: When given index is out of range.

        """
        if i is not None:
            return self[i]

        stack = self._leaves.copy()
        while len(stack) > 1:
            nodes = deque()    # Data structure to keep intermediate nodes.
            # Take leaves by groups of 2.
            for left, right in zip_longest(*([iter(stack)] * 2)):
                hash = self._hash.copy()

                hash.update(left)
                if right is not None:
                    hash.update(right)

                nodes.append(hash.digest())
            # end for
            stack = nodes.copy()
        # end while

        # If the stack is empty, we return the digest of the base hash.
        try:
            return stack.pop()
        except IndexError:
            return self._hash.digest()


    def hexdigest(self, i=None):
        """Like :meth:`~kado.utils.htree.Htree.digest` except the digest is
        returned as a string object of double length, containing only
        hexadecimal digits.

        This may be used to exchange the value safely in email or other
        non-binary environments.


        :param i: If given, returns the digest of the data for the leaf at this
                  index.
        :type i: python:int


        :returns: A hexadecimal string digest of the data.
        :rtype: python:str


        :raises IndexError: When given index is out of range.

        """
        return self.digest(i).hex()


    def update(self, data):
        """Update the hash tree object with the bytes-like object.


        :param data: Leaf data to be added to the tree.
        :type data: python:bytes


        :raises TypeError: When given data does not support the buffer protocol.

        """
        return self.append(data)


    def clear(self):
        """Remove all leaves from the tree."""
        self._leaves.clear()


    def append(self, data):
        """Add a new leaf to the right side of the tree.


        :param data: Leaf data to be added to the tree.
        :type data: python:bytes


        :raises TypeError: When given data does not support the buffer protocol.

        """
        self._leaves.append(self._data_digest(data))


    def extend(self, iterable):
        """Extend the right side of the tree by appending elements from the
        given iterable.


        :param iterable: An iterable with the data to be added to the tree.
        :type iterable: ~collections.abc.Iterable


        :raises TypeError: When given iterable does not contain data supporting
                           the buffer protocol.

        """
        self._leaves.extend(map(self._data_digest, iterable))


    def insert(self, i, data):
        """Insert a new leaf at the given index.


        :param i: Index at which the leaf must be inserted.
        :type i: python:int

        :param data: Leaf data to be inserted into the tree.
        :type data: python:bytes


        :raises IndexError: When given index is out of range.

        :raises TypeError: When given data does not support the buffer protocol.

        """
        # Force to throw IndexError if out of range.
        self._leaves[i]
        self._leaves.insert(i, self._data_digest(data))


    def pop(self, i=None):
        """Remove and return an element from the right side of the tree.


        :param i: Index of the leaf to be removed.
        :type i: python:int


        :returns: A bytes digest of the data for the the removed leaf.
        :rtype: python:bytes


        :raises IndexError: When no elements are present into the tree.

        """
        if i is None:
            return self._leaves.pop()
        else:
            item = self._leaves[i]
            del self[i]

            return item
