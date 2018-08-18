# tests/utils/test_iterator.py
# ============================
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

from kado.utils import iterator


class TestXLast(unittest.TestCase):
    """Test case for :func:`kado.utils.iterator.xlast`."""

    def test_xlast_list_empty(self):
        """Given an empty list no items should be returned."""
        TEST_DATA = []
        EXPECTED = []

        self.assertEqual(list(iterator.xlast(TEST_DATA)), EXPECTED)


    def test_xlast_list_one(self):
        """A one item list should return no item."""
        TEST_DATA = [1]
        EXPECTED = []

        self.assertEqual(list(iterator.xlast(TEST_DATA)), EXPECTED)


    def test_xlast_list_two(self):
        """A two item list should return one item."""
        TEST_DATA = [1, 2]
        EXPECTED = [1]

        self.assertEqual(list(iterator.xlast(TEST_DATA)), EXPECTED)


    def test_xlast_string_empty(self):
        """Given an empty string no items should be returned."""
        TEST_DATA = ''
        EXPECTED = ''

        self.assertEqual(''.join(iterator.xlast(TEST_DATA)), EXPECTED)


    def test_xlast_string_one(self):
        """A one character strin should return no item."""
        TEST_DATA = '1'
        EXPECTED = ''

        self.assertEqual(''.join(iterator.xlast(TEST_DATA)), EXPECTED)


    def test_xlast_string_two(self):
        """A two item string should return one item."""
        TEST_DATA = '12'
        EXPECTED = '1'

        self.assertEqual(''.join(iterator.xlast(TEST_DATA)), EXPECTED)


class TestOneXLast(unittest.TestCase):
    """Test case for :func:`kado.utils.iterator.onexlast`."""

    def test_onexlast_list_empty(self):
        """Given an empty list no items should be returned."""
        TEST_DATA = []
        EXPECTED = []

        self.assertEqual(list(iterator.onexlast(TEST_DATA)), EXPECTED)


    def test_onexlast_list_one(self):
        """A one item list should return one item."""
        TEST_DATA = [1]
        EXPECTED = [1]

        self.assertEqual(list(iterator.onexlast(TEST_DATA)), EXPECTED)


    def test_onexlast_list_two(self):
        """A two item list should return one item."""
        TEST_DATA = [1, 2]
        EXPECTED = [1]

        self.assertEqual(list(iterator.onexlast(TEST_DATA)), EXPECTED)


    def test_onexlast_string_empty(self):
        """Given an empty string no items should be returned."""
        TEST_DATA = ''
        EXPECTED = ''

        self.assertEqual(''.join(iterator.onexlast(TEST_DATA)), EXPECTED)


    def test_onexlast_string_one(self):
        """A one character strin should return no item."""
        TEST_DATA = '1'
        EXPECTED = '1'

        self.assertEqual(''.join(iterator.onexlast(TEST_DATA)), EXPECTED)


    def test_onexlast_string_two(self):
        """A two item string should return one item."""
        TEST_DATA = '12'
        EXPECTED = '1'

        self.assertEqual(''.join(iterator.onexlast(TEST_DATA)), EXPECTED)
