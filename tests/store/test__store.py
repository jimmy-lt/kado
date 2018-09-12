# tests/store/test__store.py
# ==========================
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
import unittest

from kado.store import _store


class TestIndex(unittest.TestCase):
    """Test case for :class:`kado.store._store.Index`."""

    def setUp(self):
        """Setup test cases for :class:`kado.store._store.Index`."""
        # Index keys.
        self.KEY1 = 'KEY1'
        self.KEY2 = 'KEY2'

        # Index values.
        self.VALUE1 = 'VALUE1'
        self.VALUE2 = 'VALUE2'

        # Empty index.
        self.IX_EMPTY = _store.Index()

        # Index with one key and one stored value.
        self.IX_K1V1 = _store.Index()
        self.IX_K1V1.add(self.KEY1, self.VALUE1)

        # Index with one key and two values.
        self.IX_K1V2 = _store.Index()
        self.IX_K1V2.add(self.KEY1, self.VALUE1)
        self.IX_K1V2.add(self.KEY1, self.VALUE2)

        # Index with two keys, one value each.
        self.IX_K2V1 = _store.Index()
        self.IX_K2V1.add(self.KEY1, self.VALUE1)
        self.IX_K2V1.add(self.KEY2, self.VALUE1)

        # Index with two keys, two values each.
        self.IX_K2V2 = _store.Index()
        self.IX_K2V2.add(self.KEY1, self.VALUE1)
        self.IX_K2V2.add(self.KEY1, self.VALUE2)

        self.IX_K2V2.add(self.KEY2, self.VALUE1)
        self.IX_K2V2.add(self.KEY2, self.VALUE2)


    def test___contains___one_key(self):
        """Test one key containment in a one key index."""
        self.assertIn(self.KEY1, self.IX_K1V1)


    def test___contains___two_keys(self):
        """Test one key containment in a two keys index."""
        self.assertIn(self.KEY1, self.IX_K2V1)


    def test___contains___all_keys(self):
        """Test presence of all keys in a two keys index."""
        for key in [self.KEY1, self.KEY2]:
            with self.subTest(key=key):
                self.assertIn(key, self.IX_K2V1)


    def test___contains___invalid_key_empty(self):
        """A nonexistent key should return false on an empty index."""
        self.assertNotIn('--INVALID--', self.IX_EMPTY)


    def test___contains___invalid_key_one_key(self):
        """A nonexistent key should return false on an empty index."""
        self.assertNotIn('--INVALID--', self.IX_K1V1)


    def test___iter___empty(self):
        """Iterate over an empty index."""
        self.assertEqual(list(self.IX_EMPTY), [])


    def test___iter___two_key(self):
        """Iterate over a two keys index."""
        for key in self.IX_K2V1:
            self.assertIn(key, [self.KEY1, self.KEY2])


    def test_clear_one_key(self):
        """Clear the index with only one key stored."""
        with self.subTest(predicate=True):
            self.assertEqual(len(self.IX_K1V1), 1)

        self.IX_K1V1.clear()
        self.assertEqual(len(self.IX_K1V1), 0)


    def test_clear_one_key_two_values(self):
        """Clear the index with two values stored under the same key."""
        with self.subTest(predicate=True):
            self.assertEqual(len(self.IX_K1V2), 1)
            self.assertEqual(self.IX_K1V2.count(), 2)

        self.IX_K1V2.clear()
        self.assertEqual(len(self.IX_K1V2), 0)


    def test_clear_two_keys_one_value(self):
        """Clear the index with two keys stored."""
        with self.subTest(predicate=True):
            self.assertEqual(len(self.IX_K2V1), 2)

        self.IX_K2V1.clear()
        self.assertEqual(len(self.IX_K2V1), 0)


    def test_count_all_one_key_one_value(self):
        """Count one value stored under one key."""
        self.assertEqual(self.IX_K1V1.count(), 1)


    def test_count_all_one_key_two_values(self):
        """Count two values stored under one key."""
        self.assertEqual(self.IX_K1V2.count(), 2)


    def test_count_all_two_keys_one_value(self):
        """Count two items stored under two different keys."""
        self.assertEqual(self.IX_K2V1.count(), 2)


    def test_count_all_two_keys_two_values(self):
        """Count four values in total spread over two keys."""
        self.assertEqual(self.IX_K2V2.count(), 4)


    def test_count_key_one_value(self):
        """Count one value stored under a specified key."""
        self.assertEqual(self.IX_K1V1.count(self.KEY1), 1)


    def test_count_key_two_values(self):
        """Count two values stored under a specified key."""
        self.assertEqual(self.IX_K1V2.count(self.KEY1), 2)


    def test_count_key_each_one_value(self):
        """Count each key with one stored value."""
        for key in [self.KEY1, self.KEY2]:
            with self.subTest(key=key):
                self.assertEqual(self.IX_K2V1.count(key), 1)


    def test_count_key_each_two_values(self):
        """Count each key with two stored values."""
        for key in [self.KEY1, self.KEY2]:
            with self.subTest(key=key):
                self.assertEqual(self.IX_K2V2.count(key), 2)


    def test_get_one_value(self):
        """Get one value from the index under a specified key."""
        self.assertEqual(self.IX_K1V1.get(self.KEY1), [self.VALUE1, ])


    def test_get_one_value_is_list(self):
        """Even with one item stored, a list should be returned."""
        self.assertTrue(isinstance(self.IX_K1V1.get(self.KEY1), list))


    def test_get_two_values(self):
        """Get two values from the index under a specified key."""
        for val in self.IX_K1V2.get(self.KEY1):
            self.assertIn(val, [self.VALUE1, self.VALUE2])


    def test_get_invalid_key_empty(self):
        """Get nonexistent key should raise a ``KeyError``."""
        with self.assertRaises(KeyError):
            self.IX_EMPTY.get('--INVALID--')


    def test_get_invalid_key_one_key(self):
        """Get nonexistent key on a filled index should raise a ``KeyError``."""
        with self.assertRaises(KeyError):
            self.IX_K1V1.get('--INVALID--')


    def test_add_same_value(self):
        """Adding twice the same value should only store it once."""
        self.IX_K1V1.add(self.KEY1, self.VALUE1)
        self.assertEqual(self.IX_K1V1.get(self.KEY1), [self.VALUE1, ])


    def test_remove_key(self):
        """Remove a key from the index."""
        with self.subTest(predicate=True):
            self.assertEqual(len(self.IX_K1V1), 1)

        self.IX_K1V1.remove(self.KEY1)
        self.assertEqual(len(self.IX_K1V1), 0)


    def test_remove_invalid_key(self):
        """Removing nonexistent key should raise a ``KeyError``."""
        with self.subTest(predicate=True):
            self.assertEqual(len(self.IX_K1V1), 1)

        with self.assertRaises(KeyError):
            self.IX_K1V1.remove('--INVALID--')


    def test_remove_value(self):
        """Remove a value from an index key."""
        with self.subTest(predicate=True):
            self.assertEqual(self.IX_K1V2.count(), 2)

        self.IX_K1V2.remove(self.KEY1, self.VALUE1)
        self.assertEqual(self.IX_K1V2.get(self.KEY1), [self.VALUE2, ])


    def test_remove_invalid_value(self):
        """Remove nonexistent value should raise ``ValueError``."""
        with self.subTest(predicate=True):
            self.assertEqual(self.IX_K1V1.count(), 1)

        with self.assertRaises(ValueError):
            self.IX_K1V1.remove(self.KEY1, '--INVALID--')


    def test_remove_last_entry(self):
        """Remove last value from index entry should remove the entry itself."""
        with self.subTest(predicate=True):
            self.assertEqual(len(self.IX_K1V1), 1)
            self.assertEqual(self.IX_K1V1.count(), 1)

        self.IX_K1V1.remove(self.KEY1, self.VALUE1)

        self.assertEqual(len(self.IX_K1V1), 0)
        with self.assertRaises(KeyError):
            self.IX_K1V1.get(self.KEY1)


    def test_discard_invalid_key(self):
        """Discard of a nonexistent key should not raise ``KeyError``."""
        self.IX_K1V1.discard(key='--INVALID--')


    def test_discard_invalid_value(self):
        """Discard of a nonexistent value should not raise ``ValueError``."""
        self.IX_K1V1.discard(key=self.KEY1, value='--INVALID--')


class TestChunk(unittest.TestCase):
    """Test case for :class:`kado.store._store.Chunk`."""

    def test___init__(self):
        """Test chunk initialization."""
        TEST_DATA = b'1'
        TEST_ID = uuid.UUID('14c1130e-e81a-12b5-5612-ae6acfb29ae5')
        TEST_WHASH = '66b3d38e379784f0'
        TEST_SHASH = (
            '14c1130ee81a12b55612ae6acfb29ae54d4dfa75f2551c55ccdaf1e14369d31e'
        )

        c = _store.Chunk(TEST_DATA)
        with self.subTest(test='id'):
            self.assertEqual(c.id, TEST_ID)

        with self.subTest(test='data'):
            self.assertEqual(c.data, TEST_DATA)

        with self.subTest(test='shash'):
            self.assertEqual(c.shash, TEST_SHASH)

        with self.subTest(test='whash'):
            self.assertEqual(c.whash, TEST_WHASH)


    def test__data_set_notimplementederror(self):
        """It should not be possible to reset data of a chunk."""
        c = _store.Chunk(b'1')
        with self.assertRaises(NotImplementedError):
            c.data = b'2'


    def test__id_get(self):
        """Chunk's identifier should match data's strong hash."""
        TEST_ID = uuid.UUID('14c1130e-e81a-12b5-5612-ae6acfb29ae5')

        c = _store.Chunk(b'1')
        self.assertEqual(c._id_get(), TEST_ID)
