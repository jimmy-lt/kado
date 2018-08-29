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
