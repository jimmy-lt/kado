# tests/store/test_mixin.py
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
import unittest

from kado.store import mixin


class TestHasID(unittest.TestCase):
    """Test case for :class:`kado.store.mixin.HasID`."""

    def test_id_read_only(self):
        """The `id` property should be read-only."""
        _id = mixin.HasID()
        with self.assertRaises(AttributeError):
            _id.id = 'ID'


class TestHasData(unittest.TestCase):
    """Test case for :class:`kado.store.mixin.HasData`."""

    def test___init___expected_data(self):
        """Test data initialization with expected data type."""
        TEST_DATA = b'1'

        d = mixin.HasData(data=TEST_DATA)
        self.assertEqual(d.data, TEST_DATA)


    def test___init___no_params(self):
        """Initialization with parameters should be equivalent to ``b''``."""
        EMPTY_DATA = b''

        d = mixin.HasData()
        self.assertEqual(d.data, EMPTY_DATA)


    def test___init___data_none(self):
        """Initialization with ``None`` should raise a ``TypeError``."""
        TEST_DATA = None

        with self.assertRaises(TypeError):
            mixin.HasData(data=TEST_DATA)


    def test___init___type_error(self):
        """Invalid data type should raise a ``TypeError``."""
        TEST_DATA = 1

        with self.assertRaises(TypeError):
            mixin.HasData(data=TEST_DATA)


    def test___eq___b1_equal(self):
        """Test equality of two objects carrying ``b'1'``."""
        TEST_DATA = b'1'

        d0 = mixin.HasData(data=TEST_DATA)
        d1 = mixin.HasData(data=TEST_DATA)
        self.assertEqual(d0, d1)


    def test___eq___not_equal(self):
        """Test inequality of two objects carrying different data."""
        d0 = mixin.HasData(data=b'1')
        d1 = mixin.HasData(data=b'2')
        self.assertNotEqual(d0, d1)


    def test___eq___empty_equal(self):
        """Test equality of two empty data."""
        d0 = mixin.HasData()
        d1 = mixin.HasData()
        self.assertEqual(d0, d1)


    def test___eq___b1_equals_bytes(self):
        """Comparing with an object carrying ``b'1'`` with a bytes object."""
        TEST_DATA = b'1'

        d = mixin.HasData(data=TEST_DATA)
        self.assertEqual(d, TEST_DATA)


    def test___eq___invalid_type(self):
        """Comparing with an invalid type should raise a ``TypeError``."""
        d = mixin.HasData(data=b'1')
        with self.assertRaises(TypeError):
            self.assertEqual(d, 1)


    def test___len___b1(self):
        """Test length of data ``b'1'``."""
        TEST_DATA = b'1'

        d = mixin.HasData(data=TEST_DATA)
        self.assertEqual(len(d), 1)


    def test___len___empty(self):
        """Test length of empty data."""
        d = mixin.HasData()
        self.assertEqual(len(d), 0)


    def test_data_get(self):
        """Test ``data`` property to return carried data."""
        TEST_DATA = b'1'

        d = mixin.HasData(data=TEST_DATA)
        self.assertEqual(d.data, TEST_DATA)


    def test_data_set(self):
        """Test ``data`` property to change carried data."""
        INIT_DATA = b'1'
        NEW_DATA = b'2'

        d = mixin.HasData(data=INIT_DATA)
        d.data = NEW_DATA
        self.assertEqual(d.data, NEW_DATA)


    def test_data_set_none(self):
        """Set ``data`` property to ``None`` should raise a ``TypeError``."""
        TEST_DATA = None

        d = mixin.HasData()
        with self.assertRaises(TypeError):
            d.data = TEST_DATA


    def test_data_set_type_error(self):
        """Invalid data type should raise a ``TypeError``."""
        TEST_DATA = 1

        d = mixin.HasData()
        with self.assertRaises(TypeError):
            d.data = TEST_DATA


    def test_shash_b1(self):
        """Test weak hash value of data ``b'1'``."""
        TEST_DATA = b'1'
        SHASH_DATA = (
            '14c1130ee81a12b55612ae6acfb29ae54d4dfa75f2551c55ccdaf1e14369d31e'
        )

        d = mixin.HasData(data=TEST_DATA)
        self.assertEqual(d.shash, SHASH_DATA)


    def test_shash_empty(self):
        """Requesting weak hash with empty data."""
        TEST_DATA = b''
        SHASH_DATA = (
            'bc400036267d04573773bf75f69a253116d1e5b298e90fd6452787960870d8a9'
        )

        d = mixin.HasData(data=TEST_DATA)
        self.assertEqual(d.shash, SHASH_DATA)


    def test_shash_new_data(self):
        """Setting new data should change weak hash."""
        TEST_DATA1 = b'1'
        SHASH_DATA1 = (
            '14c1130ee81a12b55612ae6acfb29ae54d4dfa75f2551c55ccdaf1e14369d31e'
        )

        TEST_DATA2 = b'2'
        SHASH_DATA2 = (
            'e4ec00adce69421f373573fe96da3b036a5530dc10983006bdcb6f910a0bd0c2'
        )

        d = mixin.HasData(data=TEST_DATA1)
        self.assertEqual(d.shash, SHASH_DATA1)

        d.data = TEST_DATA2
        self.assertEqual(d.shash, SHASH_DATA2)


    def test_whash_b1(self):
        """Test weak hash value of data ``b'1'``."""
        TEST_DATA = b'1'
        WHASH_DATA = '66b3d38e379784f0'

        d = mixin.HasData(data=TEST_DATA)
        self.assertEqual(d.whash, WHASH_DATA)


    def test_whash_empty(self):
        """Requesting weak hash with empty data."""
        TEST_DATA = b''
        WHASH_DATA = 'd7822edb70574ea2'

        d = mixin.HasData(data=TEST_DATA)
        self.assertEqual(d.whash, WHASH_DATA)


    def test_whash_new_data(self):
        """Setting new data should change weak hash."""
        TEST_DATA1 = b'1'
        WHASH_DATA1 = '66b3d38e379784f0'

        TEST_DATA2 = b'2'
        WHASH_DATA2 = 'a2c94a523dd3e9f6'

        d = mixin.HasData(data=TEST_DATA1)
        self.assertEqual(d.whash, WHASH_DATA1)

        d.data = TEST_DATA2
        self.assertEqual(d.whash, WHASH_DATA2)


class TestHasMetadata(unittest.TestCase):
    """Test case for :class:`kado.store.mixin.HasMetadata`."""

    def test___setitem___typeerror(self):
        """A key type other than ``str`` should raise a ``TypeError``."""
        m = mixin.HasMetadata()
        with self.assertRaises(TypeError):
            m[1] = '1'


    def test___setitem___valueerror(self):
        """A value type other than ``str`` should raise a ``TypeError``."""
        m = mixin.HasMetadata()
        with self.assertRaises(ValueError):
            m['1'] = 1


    def test__key_try_typeeror(self):
        """If key is not of string type, ``TypeError`` must be raised."""
        with self.assertRaises(TypeError):
            mixin.HasMetadata._key_try(1)
