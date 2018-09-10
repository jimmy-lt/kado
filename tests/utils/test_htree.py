# tests/utils/test_htree.py
# =========================
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
import unittest

from kado.utils import htree


class TestHTree(unittest.TestCase):
    """Test case for :class:`kado.utils.htree.HTree`."""

    def test___init___hash_object(self):
        """Test tree initialization using a hash object."""
        TEST_HASH = hashlib.sha256

        h = htree.HTree(TEST_HASH)
        href = TEST_HASH()

        for attr in ['block_size', 'digest_size', 'name']:
            with self.subTest(attr=attr):
                self.assertEqual(getattr(h, attr), getattr(href, attr))


    def test___init___hash_name(self):
        """Test tree initialization using a standard library hash name."""
        TEST_HASH = 'sha256'

        h = htree.HTree(TEST_HASH)
        href = hashlib.new(TEST_HASH)

        for attr in ['block_size', 'digest_size', 'name']:
            with self.subTest(attr=attr):
                self.assertEqual(getattr(h, attr), getattr(href, attr))


    def test___init___iterable(self):
        """Test tree initialization with an iterable."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', b'2', b'3']

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        with self.subTest(length=True):
            self.assertEqual(len(h), len(TEST_DATA))

        for i, digest in enumerate(h):
            with self.subTest(data=TEST_DATA[i]):
                th = hashlib.new(TEST_HASH)
                th.update(TEST_DATA[i])

                self.assertEqual(digest, th.digest())


    def test___len___empty(self):
        """Empty tree should return a length of ``0``."""
        h = htree.HTree('sha256')
        self.assertEqual(len(h), 0)


    def test___len___one_item(self):
        """Test length of a tree with one item."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', ]

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        self.assertEqual(len(h), len(TEST_DATA))


    def test___delitem___one_item(self):
        """Remove one item from the tree."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', b'2']

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        with self.subTest(test='init'):
            self.assertEqual(len(h), len(TEST_DATA))

        del h[1]
        self.assertEqual(len(h), len(TEST_DATA) - 1)


    def test___delitem___indexerror(self):
        """Removing an out of range item should raise ``IndexError``."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', ]

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        with self.subTest(test='init'):
            self.assertEqual(len(h), len(TEST_DATA))

        with self.assertRaises(IndexError):
            del h[999]


    def test___getitem___one_item(self):
        """Get one item from the tree."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', ]

        href = hashlib.new(TEST_HASH)
        for data in TEST_DATA:
            href.update(data)

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        self.assertEqual(h[0], href.digest())


    def test___getitem___indexerror(self):
        """Getting an out of range item should raise ``IndexError``."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', ]

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        with self.subTest(test='init'):
            self.assertEqual(len(h), len(TEST_DATA))

        with self.assertRaises(IndexError):
            return h[999]


    def test___setitem___one_item(self):
        """Replace one item by other data."""
        TEST_HASH = 'sha256'

        TEST_DATA1 = [b'1', ]
        TEST_DATA2 = b'2'

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA1)
        with self.subTest(test='init'):
            href = hashlib.new(TEST_HASH)
            href.update(TEST_DATA1[0])

            self.assertEqual(h[0], href.digest())

        h[0] = TEST_DATA2
        href = hashlib.new(TEST_HASH)
        href.update(TEST_DATA2)

        self.assertEqual(h[0], href.digest())


    def test___setitem___indexerror(self):
        """Setting an out of range item should raise ``IndexError``."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', ]

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        with self.subTest(test='init'):
            self.assertEqual(len(h), len(TEST_DATA))

        with self.assertRaises(IndexError):
            h[999] = b'DATA'


    def test__data_digest(self):
        """Digested data should return same result as the bare hash object."""
        TEST_HASH = 'sha256'
        TEST_DATA = b'1'

        h = htree.HTree(TEST_HASH)
        href = hashlib.new(TEST_HASH)
        href.update(TEST_DATA)

        self.assertEqual(h._data_digest(TEST_DATA), href.digest())


    def test__data_digest_typeerror(self):
        """Non buffer protocol data should raise a ``TypeError``."""
        TEST_HASH = 'sha256'
        TEST_DATA = 1

        with self.subTest(test='init'):
            with self.assertRaises(TypeError):
                href = hashlib.new(TEST_HASH)
                href.update(TEST_DATA)

        h = htree.HTree(TEST_HASH)
        with self.assertRaises(TypeError):
            h._data_digest(TEST_DATA)


    def test_copy_empty(self):
        """Test copy of an empty tree."""
        TEST_HASH = 'sha256'

        h0 = htree.HTree(TEST_HASH)
        h1 = h0.copy()

        with self.subTest(hash_name=TEST_HASH):
            self.assertEqual(h0.name, h1.name)

        with self.subTest(test='length'):
            self.assertEqual(len(h0), len(h1))

        with self.subTest(test='digest'):
            self.assertEqual(h0.digest(), h1.digest())


    def test_copy_one_item(self):
        """Test copy of a tree with one item."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', ]

        h0 = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        h1 = h0.copy()

        with self.subTest(hash_name=TEST_HASH):
            self.assertEqual(h0.name, h1.name)

        with self.subTest(test='length'):
            self.assertEqual(len(h0), len(h1))

        with self.subTest(test='digest'):
            self.assertEqual(h0.digest(), h1.digest())


    def test_digest_empty(self):
        """Test digest of an empty tree."""
        TEST_HASH = 'sha256'

        h = htree.HTree(TEST_HASH)
        href = hashlib.new(TEST_HASH)

        self.assertEqual(h.digest(), href.digest())


    def test_digest_one_item(self):
        """Test digest of a one item tree."""
        TEST_HASH = hashlib.sha256

        # Data block.
        l0 = b'0'

        # Manual tree.
        #
        # hash(l0)
        root = TEST_HASH(l0)

        # HTree.
        h = htree.HTree(TEST_HASH)
        h.update(l0)

        self.assertEqual(h.digest(), root.digest())


    def test_digest_two_items(self):
        """Test digest of a two items tree."""
        TEST_HASH = hashlib.sha256

        # Data blocks.
        d0 = b'0'
        d1 = b'1'

        # Manual tree.
        #
        # hash(
        #     hash(l0) + hash(l1)
        # )
        l0 = TEST_HASH(d0).digest()
        l1 = TEST_HASH(d1).digest()

        root = TEST_HASH()
        root.update(l0)
        root.update(l1)

        # HTree.
        h = htree.HTree(TEST_HASH)
        h.update(d0)
        h.update(d1)

        self.assertEqual(h.digest(), root.digest())


    def test_digest_three_items(self):
        """Test digest of a three items tree."""
        TEST_HASH = hashlib.sha256

        # Data blocks.
        d0 = b'0'
        d1 = b'1'
        d2 = b'2'

        # Manual tree.
        #
        # hash(
        #     hash(
        #         hash(l0) + hash(l1)
        #     )
        #     hash(
        #         hash(l2)
        #     )
        # )
        l0 = TEST_HASH(d0).digest()
        l1 = TEST_HASH(d1).digest()
        l2 = TEST_HASH(d2).digest()

        n1 = TEST_HASH()
        n1.update(l2)

        n0 = TEST_HASH()
        n0.update(l0)
        n0.update(l1)

        root = TEST_HASH()
        root.update(n0.digest())
        root.update(n1.digest())

        # HTree.
        h = htree.HTree(TEST_HASH)
        h.update(d0)
        h.update(d1)
        h.update(d2)

        self.assertEqual(h.digest(), root.digest())


    def test_digest_four_items(self):
        """Test digest of a four items tree."""
        TEST_HASH = hashlib.sha256

        # Data blocks.
        d0 = b'0'
        d1 = b'1'
        d2 = b'2'
        d3 = b'3'

        # Manual tree.
        #
        # hash(
        #     hash(
        #         hash(l0) + hash(l1)
        #     )
        #     hash(
        #         hash(l2) + hash(l3)
        #     )
        # )
        l0 = TEST_HASH(d0).digest()
        l1 = TEST_HASH(d1).digest()
        l2 = TEST_HASH(d2).digest()
        l3 = TEST_HASH(d3).digest()

        n1 = TEST_HASH()
        n1.update(l2)
        n1.update(l3)

        n0 = TEST_HASH()
        n0.update(l0)
        n0.update(l1)

        root = TEST_HASH()
        root.update(n0.digest())
        root.update(n1.digest())

        # HTree.
        h = htree.HTree(TEST_HASH)
        h.update(d0)
        h.update(d1)
        h.update(d2)
        h.update(d3)

        self.assertEqual(h.digest(), root.digest())


    def test_digest_five_items(self):
        """Test digest of a five items tree."""
        TEST_HASH = hashlib.sha256

        # Data blocks.
        d0 = b'0'
        d1 = b'1'
        d2 = b'2'
        d3 = b'3'
        d4 = b'4'

        # Manual tree.
        #
        # hash(
        #     hash(
        #         hash(
        #             hash(l0) + hash(l1)
        #         )
        #         hash(
        #             hash(l2) + hash(l3)
        #         )
        #     )
        #     hash(
        #         hash(
        #             hash(l4)
        #         )
        #     )
        # )
        l0 = TEST_HASH(d0).digest()
        l1 = TEST_HASH(d1).digest()
        l2 = TEST_HASH(d2).digest()
        l3 = TEST_HASH(d3).digest()
        l4 = TEST_HASH(d4).digest()

        n4 = TEST_HASH()
        n4.update(l4)

        n3 = TEST_HASH()
        n3.update(l2)
        n3.update(l3)

        n2 = TEST_HASH()
        n2.update(l0)
        n2.update(l1)

        n1 = TEST_HASH()
        n1.update(n4.digest())

        n0 = TEST_HASH()
        n0.update(n2.digest())
        n0.update(n3.digest())

        root = TEST_HASH()
        root.update(n0.digest())
        root.update(n1.digest())

        # HTree.
        h = htree.HTree(TEST_HASH)
        h.update(d0)
        h.update(d1)
        h.update(d2)
        h.update(d3)
        h.update(d4)

        self.assertEqual(h.digest(), root.digest())


    def test_hexdigest_empty(self):
        """Test hexadecimal digest of an empty tree."""
        TEST_HASH = 'sha256'

        h = htree.HTree(TEST_HASH)
        href = hashlib.new(TEST_HASH)

        self.assertEqual(h.hexdigest(), href.hexdigest())


    def test_hexdigest_one_item(self):
        """Test hexadecimal digest of a one item tree."""
        TEST_HASH = hashlib.sha256

        # Data block.
        l0 = b'0'

        # Manual tree.
        #
        # hash(l0)
        root = TEST_HASH(l0)

        # HTree.
        h = htree.HTree(TEST_HASH)
        h.update(l0)

        self.assertEqual(h.hexdigest(), root.hexdigest())


    def test_update_add_item(self):
        """Ensure that the item is added to the tree."""
        TEST_HASH = 'sha256'
        TEST_DATA = b'1'

        h = htree.HTree(TEST_HASH)
        with self.subTest(test='init'):
            self.assertEqual(len(h), 0)

        h.update(TEST_DATA)
        self.assertEqual(len(h), 1)


    def test_update_item_hash(self):
        """Ensure that the item is properly hashed."""
        TEST_HASH = hashlib.sha256
        TEST_DATA = b'1'

        h = htree.HTree(TEST_HASH)
        href = TEST_HASH()
        with self.subTest(test='init'):
            self.assertEqual(h.digest(), href.digest())

        h.update(TEST_DATA)
        href.update(TEST_DATA)
        self.assertEqual(h.digest(), href.digest())


    def test_update_typeeror(self):
        """Adding a non buffer protocol data should raise a ``TypeError``."""
        TEST_HASH = 'sha256'
        TEST_DATA = 1

        h = htree.HTree(TEST_HASH)
        with self.assertRaises(TypeError):
            h.update(TEST_DATA)


    def test_clear(self):
        """Ensure all items are removed from the tree."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', ]

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        with self.subTest(test='init'):
            self.assertEqual(len(h), len(TEST_DATA))

        h.clear()
        self.assertEqual(len(h), 0)


    def test_append_add_item(self):
        """Ensure that the item is added to the tree."""
        TEST_HASH = 'sha256'
        TEST_DATA = b'1'

        h = htree.HTree(TEST_HASH)
        with self.subTest(test='init'):
            self.assertEqual(len(h), 0)

        h.append(TEST_DATA)
        self.assertEqual(len(h), 1)


    def test_append_item_hash(self):
        """Ensure that the item is properly hashed."""
        TEST_HASH = hashlib.sha256
        TEST_DATA = b'1'

        h = htree.HTree(TEST_HASH)
        href = TEST_HASH()
        with self.subTest(test='init'):
            self.assertEqual(h.digest(), href.digest())

        h.append(TEST_DATA)
        href.update(TEST_DATA)
        self.assertEqual(h.digest(), href.digest())


    def test_append_typeeror(self):
        """Adding a non buffer protocol data should raise a ``TypeError``."""
        TEST_HASH = 'sha256'
        TEST_DATA = 1

        h = htree.HTree(TEST_HASH)
        with self.assertRaises(TypeError):
            h.append(TEST_DATA)


    def test_extend_add_item(self):
        """Ensure that the item is added to the tree."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', ]

        h = htree.HTree(TEST_HASH)
        with self.subTest(test='init'):
            self.assertEqual(len(h), 0)

        h.extend(TEST_DATA)
        self.assertEqual(len(h), 1)


    def test_extend_item_hash(self):
        """Ensure that the item is properly hashed."""
        TEST_HASH = hashlib.sha256
        TEST_DATA = [b'1', ]

        h = htree.HTree(TEST_HASH)
        href = TEST_HASH()
        with self.subTest(test='init'):
            self.assertEqual(h.digest(), href.digest())

        h.extend(TEST_DATA)
        for data in TEST_DATA:
            href.update(data)
        self.assertEqual(h.digest(), href.digest())


    def test_extend_typeeror(self):
        """Adding a non buffer protocol data should raise a ``TypeError``."""
        TEST_HASH = 'sha256'
        TEST_DATA = [1, ]

        h = htree.HTree(TEST_HASH)
        with self.assertRaises(TypeError):
            h.extend(TEST_DATA)


    def test_insert_len(self):
        """Insert one item into the tree."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', ]

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        with self.subTest(test='init'):
            self.assertEqual(len(h), len(TEST_DATA))

        h.insert(0, b'0')
        self.assertEqual(len(h), 2)


    def test_insert_indexerror(self):
        """Inserting an item out of range should raise ``IndexError``."""
        TEST_HASH = 'sha256'

        h = htree.HTree(TEST_HASH)
        with self.assertRaises(IndexError):
            h.insert(999, b'1')


    def test_pop_last_item(self):
        """Get the last item from the tree."""
        TEST_HASH = 'sha256'
        TEST_DATA = [b'1', ]

        hempty = hashlib.new(TEST_HASH)

        hinit = hashlib.new(TEST_HASH)
        for data in TEST_DATA:
            hinit.update(data)

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        with self.subTest(test='init hash'):
            self.assertEqual(h.digest(), hinit.digest())

        item = h.pop()
        with self.subTest(test='pop'):
            self.assertEqual(item, hinit.digest())

        with self.subTest(test='length'):
            self.assertEqual(len(h), 0)

        with self.subTest(test='empty hash'):
            self.assertEqual(h.digest(), hempty.digest())


    def test_pop_item_index(self):
        """Get an item at given index from the tree."""
        TEST_HASH = hashlib.sha256
        TEST_DATA = [b'1', b'2']

        hb1 = TEST_HASH(b'1')
        hb2 = TEST_HASH(b'2')

        hinit = TEST_HASH()
        for data in TEST_DATA:
            hinit.update(TEST_HASH(data).digest())

        h = htree.HTree(TEST_HASH, iterable=TEST_DATA)
        with self.subTest(test='init hash'):
            self.assertEqual(h.digest(), hinit.digest())

        item = h.pop(0)
        with self.subTest(test='pop'):
            self.assertEqual(item, hb1.digest())

        with self.subTest(test='length'):
            self.assertEqual(len(h), 1)

        with self.subTest(test='remaining hash'):
            self.assertEqual(h.digest(), hb2.digest())


    def test_pop_empty_indexerror(self):
        """Trying to pop an item from empty tree should raise ``IndexError``."""
        TEST_HASH = hashlib.sha256

        h = htree.HTree(TEST_HASH)
        with self.assertRaises(IndexError):
            h.pop()


    def test_pop_indexerror(self):
        """Trying to pop an out of range item should raise ``IndexError``."""
        TEST_HASH = hashlib.sha256

        h = htree.HTree(TEST_HASH)
        with self.assertRaises(IndexError):
            h.pop(999)
