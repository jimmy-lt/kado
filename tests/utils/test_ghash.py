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


    def test_cut_data_rand(self):
        """Test cutting point of known random data files."""
        TEST_DATA = [
            (8192, 'data/rand8kb.bin'),
            (4515, 'data/rand64kb.bin'),
            (8317, 'data/rand128kb.bin'),
            (8725, 'data/rand256kb.bin'),
        ]

        for ct_point, name in TEST_DATA:
            with self.subTest(file=name):
                with pkg_resources.resource_stream('tests.lib', name) as fp:
                    self.assertEqual(ghash.cut(fp.read()), ct_point)


    def test_cut_data_zero(self):
        """Test cutting point of known zeros filled data files."""
        TEST_DATA = [
            ( 8192, 'data/zero8kb.bin'),
            (65536, 'data/zero64kb.bin'),
            (65536, 'data/zero128kb.bin'),
            (65536, 'data/zero256kb.bin'),
        ]

        for ct_point, name in TEST_DATA:
            with self.subTest(file=name):
                with pkg_resources.resource_stream('tests.lib', name) as fp:
                    self.assertEqual(ghash.cut(fp.read()), ct_point)


class TestChop(unittest.TestCase):
    """Test case for :func:`kado.utils.ghash.chop`."""

    def test_chop_data_len(self):
        """Last chunk index should match the data length."""
        TEST_FILE = [
            'data/rand8kb.bin',
            'data/rand64kb.bin',
            'data/rand128kb.bin',
            'data/rand256kb.bin',
            'data/zero8kb.bin',
            'data/zero64kb.bin',
            'data/zero128kb.bin',
            'data/zero256kb.bin',
        ]

        for f in TEST_FILE:
            with pkg_resources.resource_stream('tests.lib', f) as fp:
                content = fp.read()
                last = 0
                for _, end, _ in ghash.chop(content):
                    last = end

                with self.subTest(file=f):
                    self.assertEqual(last, len(content))


    def test_chop_data_rand8kb(self):
        """Chop a known 8KB random data file."""
        TEST_FILE = 'data/rand8kb.bin'
        DATA = [
            (0, 8192, 'dd6f4e2b8e4ce06d4502326f627b7e0ee88cee48e70def44dfa448aed6476b92'),
        ]

        with pkg_resources.resource_stream('tests.lib', TEST_FILE) as fp:
            for idx, data in enumerate(ghash.chop(fp.read())):
                with self.subTest(index=idx):
                    self.assertEqual(
                        DATA[idx],
                        (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                    )


    def test_chop_data_rand64kb(self):
        """Chop a known 64KB random data file."""
        TEST_FILE = 'data/rand64kb.bin'
        DATA = [
            (    0,  4515, '6f42c414f0eb3e6054ce59d5907e71ef51072687792d992506eec0171e85a8af'),
            ( 4515, 18009, 'efdcd2871985a3758e795432fa99f89e2a5a1fb6b9ac20e228a7f931e515ea2f'),
            (18009, 27789, '0364e120290cc729c6adad8ee7dda2bc455c18cbd98eca3512bd7f3dd21a0954'),
            (27789, 36135, '9f020adb109e6dc35b60623b48f9d3b29c4405489e2b239e1e45ec0cddce3c42'),
            (36135, 46576, 'ea996bb12b9f7afef310b8e9f8868efff1a06183fef3af0892fbc88fe7defec4'),
            (46576, 61001, '1bdfa4bf5d3b8cebd194bbb39fe29b30bfea4febe1f018d36c1d4aded7e2aa6b'),
            (61001, 65536, 'cc1674a87872a0a9faba78e5adee0d9e3e3fbc2c5539af40571d073481057650'),
        ]

        with pkg_resources.resource_stream('tests.lib', TEST_FILE) as fp:
            for idx, data in enumerate(ghash.chop(fp.read())):
                with self.subTest(index=idx):
                    self.assertEqual(
                        DATA[idx],
                        (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                    )


    def test_chop_data_rand128kb(self):
        """Chop a known 128KB random data file."""
        TEST_FILE = 'data/rand128kb.bin'
        DATA = [
            (     0,   8317, '94112e37c23385ee5f012cc86b530bf1ac52c78e9c39e2bc5ddaf222f9cf4508'),
            (  8317,  17688, 'd6be177ff53d96d339e62a317ddb04ab6ae54cd3051e1624f6e697623793cc8b'),
            ( 17688,  28372, 'f811ce3783e5e1cf8a59989a5fd37e7e410822a0a5ffb2a28a604b01baee7ed6'),
            ( 28372,  39279, '287f720b0472d809b9bde7ca681a16c74aedc9e943b93870bf427c214a8a16e9'),
            ( 39279,  47683, 'acfa531572792a2b07c4037cab65db6cff97a3ba34bda5bef4305a607552ee88'),
            ( 47683,  52649, 'bc63aa96586b4657d24df2928bff6cdb7ee764d8053b47741c149efc1fac44d5'),
            ( 52649,  62986, '3fd78f7b9ece36b5879fca3d4cd9d680b7c6652d23936c1503917011a1da5cd9'),
            ( 62986,  73221, 'b3fa20565fd23119550359696d94b7343a884623ea314229e7c54a3494ff62d9'),
            ( 73221,  86967, 'b28182174b4ac2499dd8e2718cec68a348712de94f2ce4fc4302a1ae1adf3061'),
            ( 86967,  97426, 'a6b34e1c91995d02121a791540d9975b96f31d9df9a824b28071ce022705820d'),
            ( 97426, 107753, '6333aeee040778e4b494775d2b6bfcad632ab42b16aec0e7d61c68bd1c9c4c64'),
            (107753, 120049, '578ba5ad46b14ce8fd4bcb80298df8d5f735155305c6359b7ece93500fd85812'),
            (120049, 128568, 'be4e1e6164725199d3d164b0191d4122c48b37ef24dcb6f34768fc7c3cce333b'),
            (128568, 131072, '48d0deac5e7d91796de75f58210c76d65dbffcd991daaf1ffdc3798f23dac229'),
        ]

        with pkg_resources.resource_stream('tests.lib', TEST_FILE) as fp:
            for idx, data in enumerate(ghash.chop(fp.read())):
                with self.subTest(index=idx):
                    self.assertEqual(
                        DATA[idx],
                        (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                    )


    def test_chop_data_rand256kb(self):
        """Chop a known 256KB random data file."""
        TEST_FILE = 'data/rand256kb.bin'
        DATA = [
            (     0,   8725, '82fd495cd62f39424c587ff335662872bd846be44feb024d7129d593a93e4d87'),
            (  8725,  18915, 'f5748eba459bedb8148629274f7458e6c0070d88899d6a531912d9f9764ec010'),
            ( 18915,  28168, '739c332e105853dcb654c3da0da14fd87fa848cecf58c884e89c575c71551dde'),
            ( 28168,  39002, 'a136f68ebaddff1e5dc6905cb0e27f6d834a07d257f41c549e58a20027141680'),
            ( 39002,  51566, '7e2986959dfdd55de1c02594c277b5ca58d83df7a0536dea30c631e20d221c07'),
            ( 51566,  70863, '31716ae893da9b6df371db8ba4e78d7f724919bf9cdce42ab3e067a80bcae720'),
            ( 70863,  79112, 'b9489fb19eadd7d216c600f6179d6047f06c9701108baaf0d6177e23621531b1'),
            ( 79112,  88414, 'f2f51cafbdbf51b428b2dbbe67d7388c6c1cbeb7747b5eedd0fe50cd30f4ff5f'),
            ( 88414,  99125, '071be582a49a9a29a439ae045e95825eebf985c4080f89c2666193369b3fb26e'),
            ( 99125, 106020, 'a3e0cc02c9a0a2c8763b3ae31520548ad8581696f28649c12965f5ed64968b8c'),
            (106020, 116428, '24aecf832cdaa68271e21c6c45c8961d186ff94d2e53f02b14a8924078c123a8'),
            (116428, 125122, 'f43b90b369887c27685a5d639ca66a24049652c088de78649834c900c4c6dfb2'),
            (125122, 135525, '19f4851fd07b7edc14d01b608399f9541712b2395791c7d8341bf60a81334d1b'),
            (135525, 144839, '799ede4c1139c24b28c4d7e365f4a29befd4795747b81f18d07c43e320ad9f27'),
            (144839, 153947, '18853c6e34e9ef384a70601a44b6632a1b13bb5657ee2d8e0de1caa2de080404'),
            (153947, 168953, '4848d6736fcc2b2216e2d4919fc0a0ebf2d858c95b8fe798d34a9185d1d46603'),
            (168953, 177155, 'd169c8abdf90370113f54780d150b74b9b85e90bd30ef67b9104c7bcb40391e2'),
            (177155, 185374, '3e4746ad20f19c84d9b4acebf55b7f4277fbfc170120a3945fa0dbfba6cb2490'),
            (185374, 196826, 'aa16e38b56b4c9efc03d100f8d2129efa2d21f84aa005c9cd6c74242763ba2f3'),
            (196826, 208163, '558b6a2c0ca610f0e4ff73854c6737eee8b04f2f55e1ff60cf567c12ee55ce00'),
            (208163, 223455, '8f1f919529217a0195960a19ef863f7a85e249958c3eb3e1665c9e67682fb804'),
            (223455, 238114, '0ccb646109ce14ae15b5b77ec19a8ca0f6a6e21ffe92fa831bd7fabc716c2601'),
            (238114, 245210, 'f9e0e8e6a683e0d72540df95e9310b9d7976e83b5ee8d1d67d456185ad5a25e3'),
            (245210, 248914, 'c7bc320808bce171058ec5aa0a12ecc0370e24b61a2972c972f2b93207422c0b'),
            (248914, 257229, '99c1967d62545e9d095551442189de8d465b24b0f811d7b0942b2c61b8cabe36'),
            (257229, 262144, '73f0cee2478e92361c17c7e35030902e51baa8e4097662370c6bc1a627c7b5f3'),
        ]

        with pkg_resources.resource_stream('tests.lib', TEST_FILE) as fp:
            for idx, data in enumerate(ghash.chop(fp.read())):
                with self.subTest(index=idx):
                    self.assertEqual(
                        DATA[idx],
                        (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                    )


    def test_chop_data_zero8kb(self):
        """Chop a known 8KB zeros filled data file."""
        TEST_FILE = 'data/zero8kb.bin'
        DATA = [
            (0, 8192, '9f1dcbc35c350d6027f98be0f5c8b43b42ca52b7604459c0c42be3aa88913d47'),
        ]

        with pkg_resources.resource_stream('tests.lib', TEST_FILE) as fp:
            for idx, data in enumerate(ghash.chop(fp.read())):
                with self.subTest(index=idx):
                    self.assertEqual(
                        DATA[idx],
                        (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                    )


    def test_chop_data_zero64kb(self):
        """Chop a known 64KB zeros filled data file."""
        TEST_FILE = 'data/zero64kb.bin'
        DATA = [
            (0, 65536, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
        ]

        with pkg_resources.resource_stream('tests.lib', TEST_FILE) as fp:
            for idx, data in enumerate(ghash.chop(fp.read())):
                with self.subTest(index=idx):
                    self.assertEqual(
                        DATA[idx],
                        (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                    )


    def test_chop_data_zero128kb(self):
        """Chop a known 128KB zeros filled data file."""
        TEST_FILE = 'data/zero128kb.bin'
        DATA = [
            (    0,  65536, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
            (65536, 131072, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
        ]

        with pkg_resources.resource_stream('tests.lib', TEST_FILE) as fp:
            for idx, data in enumerate(ghash.chop(fp.read())):
                with self.subTest(index=idx):
                    self.assertEqual(
                        DATA[idx],
                        (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                    )


    def test_chop_data_zero256kb(self):
        """Chop a known 256KB zeros filled data file."""
        TEST_FILE = 'data/zero256kb.bin'
        DATA = [
            (     0,  65536, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
            ( 65536, 131072, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
            (131072, 196608, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
            (196608, 262144, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
        ]

        with pkg_resources.resource_stream('tests.lib', TEST_FILE) as fp:
            for idx, data in enumerate(ghash.chop(fp.read())):
                with self.subTest(index=idx):
                    self.assertEqual(
                        DATA[idx],
                        (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                    )


class TestRead(unittest.TestCase):
    """Test case for :func:`kado.utils.ghash.read`."""

    def test_read_data_len(self):
        """Last chunk index should match the data length."""
        TEST_FILE = [
            'data/rand8kb.bin',
            'data/rand64kb.bin',
            'data/rand128kb.bin',
            'data/rand256kb.bin',
            'data/zero8kb.bin',
            'data/zero64kb.bin',
            'data/zero128kb.bin',
            'data/zero256kb.bin',
        ]

        for f in TEST_FILE:
            with pkg_resources.resource_stream('tests.lib', f) as fp:
                l_content = len(fp.read())

            last = 0
            for _, end, _ in ghash.read(
                pkg_resources.resource_filename('tests.lib', f)
            ):
                last = end

            with self.subTest(file=f):
                self.assertEqual(last, l_content)


    def test_read_data_rand8kb(self):
        """Read and chop a known 8KB random data file."""
        TEST_FILE = 'data/rand8kb.bin'
        DATA = [
            (0, 8192, 'dd6f4e2b8e4ce06d4502326f627b7e0ee88cee48e70def44dfa448aed6476b92'),
        ]

        for idx, data in enumerate(ghash.read(
            pkg_resources.resource_filename('tests.lib', TEST_FILE)
        )):
            with self.subTest(i=idx):
                self.assertEqual(
                    DATA[idx],
                    (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                )


    def test_read_data_rand64kb(self):
        """Read and chop a known 64KB random data file."""
        TEST_FILE = 'data/rand64kb.bin'
        DATA = [
            (    0,  4515, '6f42c414f0eb3e6054ce59d5907e71ef51072687792d992506eec0171e85a8af'),
            ( 4515, 18009, 'efdcd2871985a3758e795432fa99f89e2a5a1fb6b9ac20e228a7f931e515ea2f'),
            (18009, 27789, '0364e120290cc729c6adad8ee7dda2bc455c18cbd98eca3512bd7f3dd21a0954'),
            (27789, 36135, '9f020adb109e6dc35b60623b48f9d3b29c4405489e2b239e1e45ec0cddce3c42'),
            (36135, 46576, 'ea996bb12b9f7afef310b8e9f8868efff1a06183fef3af0892fbc88fe7defec4'),
            (46576, 61001, '1bdfa4bf5d3b8cebd194bbb39fe29b30bfea4febe1f018d36c1d4aded7e2aa6b'),
            (61001, 65536, 'cc1674a87872a0a9faba78e5adee0d9e3e3fbc2c5539af40571d073481057650'),
        ]

        for idx, data in enumerate(ghash.read(
            pkg_resources.resource_filename('tests.lib', TEST_FILE)
        )):
            with self.subTest(index=idx):
                self.assertEqual(
                    DATA[idx],
                    (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                )


    def test_read_data_rand128kb(self):
        """Read and chop a known 128KB random data file."""
        TEST_FILE = 'data/rand128kb.bin'
        DATA = [
            (     0,   8317, '94112e37c23385ee5f012cc86b530bf1ac52c78e9c39e2bc5ddaf222f9cf4508'),
            (  8317,  17688, 'd6be177ff53d96d339e62a317ddb04ab6ae54cd3051e1624f6e697623793cc8b'),
            ( 17688,  28372, 'f811ce3783e5e1cf8a59989a5fd37e7e410822a0a5ffb2a28a604b01baee7ed6'),
            ( 28372,  39279, '287f720b0472d809b9bde7ca681a16c74aedc9e943b93870bf427c214a8a16e9'),
            ( 39279,  47683, 'acfa531572792a2b07c4037cab65db6cff97a3ba34bda5bef4305a607552ee88'),
            ( 47683,  52649, 'bc63aa96586b4657d24df2928bff6cdb7ee764d8053b47741c149efc1fac44d5'),
            ( 52649,  62986, '3fd78f7b9ece36b5879fca3d4cd9d680b7c6652d23936c1503917011a1da5cd9'),
            ( 62986,  73221, 'b3fa20565fd23119550359696d94b7343a884623ea314229e7c54a3494ff62d9'),
            ( 73221,  86967, 'b28182174b4ac2499dd8e2718cec68a348712de94f2ce4fc4302a1ae1adf3061'),
            ( 86967,  97426, 'a6b34e1c91995d02121a791540d9975b96f31d9df9a824b28071ce022705820d'),
            ( 97426, 107753, '6333aeee040778e4b494775d2b6bfcad632ab42b16aec0e7d61c68bd1c9c4c64'),
            (107753, 120049, '578ba5ad46b14ce8fd4bcb80298df8d5f735155305c6359b7ece93500fd85812'),
            (120049, 128568, 'be4e1e6164725199d3d164b0191d4122c48b37ef24dcb6f34768fc7c3cce333b'),
            (128568, 131072, '48d0deac5e7d91796de75f58210c76d65dbffcd991daaf1ffdc3798f23dac229'),
        ]

        for idx, data in enumerate(ghash.read(
            pkg_resources.resource_filename('tests.lib', TEST_FILE)
        )):
            with self.subTest(index=idx):
                self.assertEqual(
                    DATA[idx],
                    (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                )


    def test_read_data_rand256kb(self):
        """Read and chop a known 256KB random data file."""
        TEST_FILE = 'data/rand256kb.bin'
        DATA = [
            (     0,   8725, '82fd495cd62f39424c587ff335662872bd846be44feb024d7129d593a93e4d87'),
            (  8725,  18915, 'f5748eba459bedb8148629274f7458e6c0070d88899d6a531912d9f9764ec010'),
            ( 18915,  28168, '739c332e105853dcb654c3da0da14fd87fa848cecf58c884e89c575c71551dde'),
            ( 28168,  39002, 'a136f68ebaddff1e5dc6905cb0e27f6d834a07d257f41c549e58a20027141680'),
            ( 39002,  51566, '7e2986959dfdd55de1c02594c277b5ca58d83df7a0536dea30c631e20d221c07'),
            ( 51566,  70863, '31716ae893da9b6df371db8ba4e78d7f724919bf9cdce42ab3e067a80bcae720'),
            ( 70863,  79112, 'b9489fb19eadd7d216c600f6179d6047f06c9701108baaf0d6177e23621531b1'),
            ( 79112,  88414, 'f2f51cafbdbf51b428b2dbbe67d7388c6c1cbeb7747b5eedd0fe50cd30f4ff5f'),
            ( 88414,  99125, '071be582a49a9a29a439ae045e95825eebf985c4080f89c2666193369b3fb26e'),
            ( 99125, 106020, 'a3e0cc02c9a0a2c8763b3ae31520548ad8581696f28649c12965f5ed64968b8c'),
            (106020, 116428, '24aecf832cdaa68271e21c6c45c8961d186ff94d2e53f02b14a8924078c123a8'),
            (116428, 125122, 'f43b90b369887c27685a5d639ca66a24049652c088de78649834c900c4c6dfb2'),
            (125122, 135525, '19f4851fd07b7edc14d01b608399f9541712b2395791c7d8341bf60a81334d1b'),
            (135525, 144839, '799ede4c1139c24b28c4d7e365f4a29befd4795747b81f18d07c43e320ad9f27'),
            (144839, 153947, '18853c6e34e9ef384a70601a44b6632a1b13bb5657ee2d8e0de1caa2de080404'),
            (153947, 168953, '4848d6736fcc2b2216e2d4919fc0a0ebf2d858c95b8fe798d34a9185d1d46603'),
            (168953, 177155, 'd169c8abdf90370113f54780d150b74b9b85e90bd30ef67b9104c7bcb40391e2'),
            (177155, 185374, '3e4746ad20f19c84d9b4acebf55b7f4277fbfc170120a3945fa0dbfba6cb2490'),
            (185374, 196826, 'aa16e38b56b4c9efc03d100f8d2129efa2d21f84aa005c9cd6c74242763ba2f3'),
            (196826, 208163, '558b6a2c0ca610f0e4ff73854c6737eee8b04f2f55e1ff60cf567c12ee55ce00'),
            (208163, 223455, '8f1f919529217a0195960a19ef863f7a85e249958c3eb3e1665c9e67682fb804'),
            (223455, 238114, '0ccb646109ce14ae15b5b77ec19a8ca0f6a6e21ffe92fa831bd7fabc716c2601'),
            (238114, 245210, 'f9e0e8e6a683e0d72540df95e9310b9d7976e83b5ee8d1d67d456185ad5a25e3'),
            (245210, 248914, 'c7bc320808bce171058ec5aa0a12ecc0370e24b61a2972c972f2b93207422c0b'),
            (248914, 257229, '99c1967d62545e9d095551442189de8d465b24b0f811d7b0942b2c61b8cabe36'),
            (257229, 262144, '73f0cee2478e92361c17c7e35030902e51baa8e4097662370c6bc1a627c7b5f3'),
        ]

        for idx, data in enumerate(ghash.read(
            pkg_resources.resource_filename('tests.lib', TEST_FILE)
        )):
            with self.subTest(index=idx):
                self.assertEqual(
                    DATA[idx],
                    (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                )


    def test_read_data_zero8kb(self):
        """Read and chop a known 8KB zeros filled data file."""
        TEST_FILE = 'data/zero8kb.bin'
        DATA = [
            (0, 8192, '9f1dcbc35c350d6027f98be0f5c8b43b42ca52b7604459c0c42be3aa88913d47'),
        ]

        for idx, data in enumerate(ghash.read(
            pkg_resources.resource_filename('tests.lib', TEST_FILE)
        )):
            with self.subTest(index=idx):
                self.assertEqual(
                    DATA[idx],
                    (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                )


    def test_read_data_zero64kb(self):
        """Read and chop a known 64KB zeros filled data file."""
        TEST_FILE = 'data/zero64kb.bin'
        DATA = [
            (0, 65536, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
        ]

        for idx, data in enumerate(ghash.read(
            pkg_resources.resource_filename('tests.lib', TEST_FILE)
        )):
            with self.subTest(index=idx):
                self.assertEqual(
                    DATA[idx],
                    (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                )


    def test_read_data_zero128kb(self):
        """Read and chop a known 128KB zeros filled data file."""
        TEST_FILE = 'data/zero128kb.bin'
        DATA = [
            (    0,  65536, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
            (65536, 131072, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
        ]

        for idx, data in enumerate(ghash.read(
            pkg_resources.resource_filename('tests.lib', TEST_FILE)
        )):
            with self.subTest(index=idx):
                self.assertEqual(
                    DATA[idx],
                    (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                )


    def test_read_data_zero256kb(self):
        """Read and chop a known 256KB zeros filled data file."""
        TEST_FILE = 'data/zero256kb.bin'
        DATA = [
            (     0,  65536, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
            ( 65536, 131072, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
            (131072, 196608, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
            (196608, 262144, 'de2f256064a0af797747c2b97505dc0b9f3df0de4f489eac731c23ae9ca9cc31'),
        ]

        for idx, data in enumerate(ghash.read(
            pkg_resources.resource_filename('tests.lib', TEST_FILE)
        )):
            with self.subTest(index=idx):
                self.assertEqual(
                    DATA[idx],
                    (data[0], data[1], hashlib.sha256(data[2]).hexdigest())
                )


    def test_read_eq_chop(self):
        """``read`` and ``chop`` should return the exact same data."""
        TEST_FILE = [
            'data/rand8kb.bin',
            'data/rand64kb.bin',
            'data/rand128kb.bin',
            'data/rand256kb.bin',
            'data/zero8kb.bin',
            'data/zero64kb.bin',
            'data/zero128kb.bin',
            'data/zero256kb.bin',
        ]

        for f in TEST_FILE:
            with pkg_resources.resource_stream('tests.lib', f) as fp:
                chop = [
                    (start, end, hashlib.sha256(data).hexdigest())
                    for start, end, data in ghash.chop(fp.read())
                ]

            read = [
                (start, end, hashlib.sha256(data).hexdigest())
                for start, end, data in ghash.read(
                    pkg_resources.resource_filename('tests.lib', f)
                )
            ]

            with self.subTest(file=f):
                self.assertEqual(chop, read)
