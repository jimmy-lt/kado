# tests/utils/test_ghash.py
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
import pkg_resources

import hashlib

from kado import constants as c
from kado.utils import ghash

from tests.lib import constants as tc


class TestGHash(unittest.TestCase):
    """Test case for :func:`kado.utils.ghash.ghash`."""

    def test_ghash_sequence(self):
        """Basic ``ghash`` test on a sequence of characters."""
        INIT_HASH = 0
        TEST_DATA = b'0123456789abcdefghijklmnopqrstuvwxyz'
        HASH_DATA = [
            0x192340397c988b6f, 0xefc5bc5fa4408630, 0xfb5bc99628d59ad4,
            0xe53ec3ad106555d0, 0xacd2e5528d1c8edb, 0xded83bd80e3f6a80,
            0xd4f999f0069cd46d, 0xd4583576d6033deb, 0xdc6db7c69e83e859,
            0x59a1c8d2f3490df6, 0x9d17e41d97809999, 0x88c6cbdd1a3c6ce9,
            0x962aa19bd5b0cb1e, 0x5e57e8667fde63e8, 0x6b9eafafa32707ed,
            0x1b20adeb05623a92, 0xf1a640886be62cf3, 0x05f655d4ebc1e835,
            0x177e24ea167a3da7, 0x0da18f53577cb417, 0x074828ada929b1ec,
            0x7d41698b0752fa52, 0xb71d01536265804d, 0x3f4f7448de07abf9,
            0x2dd1488ddc7c6e30, 0x2fe3573da7b77cc9, 0x55b9f117d610c05b,
            0x4db621a35cbf59ee, 0x96a2af56523d1d2f, 0xf4a744db21c8eedb,
            0xfaf92425521e6566, 0x5e1c09452e85986d, 0x9ee7e422fd0042d1,
            0x3e98973ebf9498d2, 0x84b60bd37abb6f17, 0x6e24b64e2acb1d81,
        ]

        for idx, ch in enumerate(TEST_DATA):
            with self.subTest(index=idx):
                h = ghash.ghash(INIT_HASH, ch)
                self.assertEqual(h, HASH_DATA[idx])


    def test_ghash_chained(self):
        """Basic ``ghash`` test on a chained character sequence."""
        INIT_HASH = 0
        TEST_DATA = b'0123456789abcdefghijklmnopqrstuvwxyz'
        HASH_DATA = [
            0x192340397c988b6f, 0x220c3cd29d719d0e, 0x3f74433b63b8d4f0,
            0x64274a23d7d6ffb0, 0x7521799a3cca8e3b, 0xc91b2f0c87d486f6,
            0x672ff8091645e259, 0xa2b82589028f029d, 0x21de02d8a3a1ed93,
            0x9d5dce843a8ce91c, 0xd7d381260c9a6bd1, 0x386dce293371448b,
            0x07063dee3c935434, 0x6c646442f9050c50, 0x446778359531208d,
            0xa3ef9e562fc47bac, 0x39857d34cb6f244b, 0x7901503e82a030cb,
            0x0980c5671bba9f3d, 0x20a31a218ef1f291, 0x488e5cf0c70d970e,
            0x0e5e236c956e286e, 0xd3d9482c8d41d129, 0xe70204a1f88b4e4b,
            0xfbd551d1cd930ac6, 0x278dfae142dd9255, 0xa4d5e6da5bcbe505,
            0x9761ef58145723f8, 0xc5668e067aeb651f, 0x7f7460e8179fb919,
            0xf9e1e5f5815dd798, 0x51dfd5303141479d, 0x42a78e835f82d20b,
            0xc3e7b4457e9a3ce8, 0x0c85745e77efe8e7, 0x872f9f0b1aaaef4f,
        ]

        h = INIT_HASH
        for idx, ch in enumerate(TEST_DATA):
            with self.subTest(index=idx):
                h = ghash.ghash(h, ch)
                self.assertEqual(h, HASH_DATA[idx])


class TestCut(unittest.TestCase):
    """Test case for :func:`kado.utils.ghash.cut`."""

    def test_cut_chunk_min_size_b1(self):
        """Data length lower or equal to ``GHASH_CHUNK_LO`` should not cut."""
        TEST_DATA = b'1' * c.GHASH_CHUNK_LO

        idx = ghash.cut(TEST_DATA)
        self.assertEqual(idx, c.GHASH_CHUNK_LO)


    def test_cut_chunk_max_size_b1(self):
        """Maximum chunk size should not be over ``GHASH_CHUNK_HI``."""
        TEST_DATA = b'1' * (c.GHASH_CHUNK_HI + 1)

        idx = ghash.cut(TEST_DATA)
        self.assertEqual(idx, c.GHASH_CHUNK_HI)


    def test_cut_data(self):
        """Test cutting point of known data files."""
        for name, chunks in tc.DATA_CHUNKS_SHA256.items():
            ct_point = chunks[0][1]
            with self.subTest(file=name):
                with pkg_resources.resource_stream('tests.lib', name) as fp:
                    self.assertEqual(ghash.cut(fp.read()), ct_point)


class TestChop(unittest.TestCase):
    """Test case for :func:`kado.utils.ghash.chop`."""

    def test_chop_data_len(self):
        """Last chunk index should match the data length."""
        for name in tc.DATA_CHUNKS_SHA256:
            with pkg_resources.resource_stream('tests.lib', name) as fp:
                content = fp.read()
                last = 0
                for _, end, _ in ghash.chop(content):
                    last = end

                with self.subTest(file=name):
                    self.assertEqual(last, len(content))


    def test_chop_data(self):
        """Chop known data files."""
        for name, chunks in tc.DATA_CHUNKS_SHA256.items():
            with pkg_resources.resource_stream('tests.lib', name) as fp:
                for idx, ck in enumerate(ghash.chop(fp.read())):
                    with self.subTest(file=name, index=idx):
                        self.assertEqual(
                            chunks[idx],
                            (ck[0], ck[1], hashlib.sha256(ck[2]).hexdigest())
                        )


class TestRead(unittest.TestCase):
    """Test case for :func:`kado.utils.ghash.read`."""

    def test_read_data_len(self):
        """Last chunk index should match the data length."""
        for name in tc.DATA_CHUNKS_SHA256:
            with pkg_resources.resource_stream('tests.lib', name) as fp:
                l_content = len(fp.read())

            last = 0
            for _, end, _ in ghash.read(
                    pkg_resources.resource_filename('tests.lib', name)
            ):
                last = end

            with self.subTest(file=name):
                self.assertEqual(last, l_content)

    def test_read_data(self):
        """Read and chop known data files."""
        for name, chunks in tc.DATA_CHUNKS_SHA256.items():
            for idx, ck in enumerate(ghash.read(
                pkg_resources.resource_filename('tests.lib', name)
            )):
                with self.subTest(file=name, index=idx):
                    self.assertEqual(
                        chunks[idx],
                        (ck[0], ck[1], hashlib.sha256(ck[2]).hexdigest())
                    )


    def test_read_eq_chop(self):
        """``read`` and ``chop`` should return the exact same data."""
        for name in tc.DATA_CHUNKS_SHA256:
            with pkg_resources.resource_stream('tests.lib', name) as fp:
                chop = [
                    (start, end, hashlib.sha256(data).hexdigest())
                    for start, end, data in ghash.chop(fp.read())
                ]

            read = [
                (start, end, hashlib.sha256(data).hexdigest())
                for start, end, data in ghash.read(
                    pkg_resources.resource_filename('tests.lib', name)
                )
            ]

            with self.subTest(file=name):
                self.assertEqual(chop, read)
