# kado/utils/ghash.py
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
from kado import constants as c
from kado.utils import iterator


# Source:
#    https://www.usenix.org/conference/atc16/technical-sessions/presentation/xia


def ghash(h, ch):
    """Employs an array of 256 random integers to map with the numerical value
    of the given byte.


    :param h: Current hash value.
    :type h: python:int

    :param ch: Character to be added to the hash value.
    :type ch: python:bytes


    :returns: Updated Gear hash value.
    :rtype: python:int

    """
    return ((h << 1) + c.GHASH_TABLE[ch]) & 0xffffffffffffffff


def cut(data):
    """Find the next cutting point within given data.


    :param data: Data stream to cut.
    :type data: python:bytes


    :returns: Index value at which data must be cut.
    :rtype: python:int

    """
    h = 0                     # Hash value holder.
    idx = c.GHASH_CHUNK_LO    # Set index to the minimum chunk size.

    # Mask selection sentinels.
    sentinel_md = c.GHASH_CHUNK_MD
    sentinel_hi = data_size = len(data)

    # If given data is lower than the minimum chunk size we return data length.
    if data_size <= c.GHASH_CHUNK_LO:
        return data_size

    # Evaluate appropriate sentinel value.
    if data_size >= c.GHASH_CHUNK_HI:
        sentinel_hi = c.GHASH_CHUNK_HI
    elif data_size <= c.GHASH_CHUNK_MD:
        sentinel_md = data_size

    for sentinel, mask in [
        (sentinel_md, c.GHASH_MASK_LO),
        (sentinel_hi, c.GHASH_MASK_HI),
    ]:
        while idx < sentinel:
            h = ghash(h, data[idx])
            if not h & mask:
                return idx
            idx += 1
    else:
        return idx


def chop(data):
    """Split given data stream in normalized chunks.


    :param data: Data stream to be divided.
    :type data: python:bytes


    :returns: A three items tuple with the chunk start index, the chunk length
              and the chunk data.
    :rtype: ~typing.Tuple[python:int, python:int, python:bytes]

    """
    data_size = len(data)        # Maximum length of the data.
    ck_start = 0                 # Chunk start index within the data.
    ck_end = 0                   # Chunk end index within the data.
    ct_idx = c.GHASH_CHUNK_HI    # Current cutting index.

    while ct_idx != ck_end:
        ck_end = ck_start + cut(data[ck_start:ct_idx])

        yield ck_start, ck_end, data[ck_start:ck_end]
        ck_start, ct_idx = ck_end, min(ck_end + c.GHASH_CHUNK_HI, data_size)


def read(name):
    """Read given file and split it in normalized chunks.


    :param name: Path to the file to split in chunks.
    :type name: python:str

    :returns: A three items tuple with the chunk start index, the chunk length
              and the chunk data.
    :rtype: ~typing.Tuple[python:int, python:int, python:bytes]

    """
    fp_idx = 0              # Current position in the file.
    remain = bytearray()    # Data remaining from the chunking process.
    buffer = bytearray(c.GHASH_CHUNK_HI)    # Buffer to keep file data.

    with open(name, 'rb') as fp:
        while True:
            # Load up to :data:`~kado.constants.GHASH_CHUNK_HI` file data into
            # the buffer.
            read_bytes = fp.readinto(buffer)
            if read_bytes == 0:
                # No more data? We're getting out of here.
                break

            # We prepend remaining data from previous iteration before chopping.
            buffer = remain + buffer
            # Keep in mind read data can be lower than actual buffer size.
            bf_end = read_bytes + len(remain)

            # :func:`~kado.utils.ghash.chop` will cut all given data, however
            # the last chunk may not be the end of the file and we may still
            # have some more data to read.
            #
            # Therefore, we keep the last chunk aside looking for a potential
            # bigger chunk.
            ck_idx = 0
            for ck_start, ck_end, ck_data in iterator.xlast(
                chop(buffer[:bf_end])
            ):
                yield fp_idx + ck_start, fp_idx + ck_end, bytes(ck_data)
                ck_idx = ck_end

            # Saving the last chunk of data for the next iteration.
            remain = buffer[ck_idx:bf_end]
            buffer = bytearray(c.GHASH_CHUNK_HI - len(remain))

            # Raising our file index.
            fp_idx += ck_idx

        # We're done reading the file, chopping remaining data.
        for ck_start, ck_end, ck_data in chop(remain):
            yield fp_idx + ck_start, fp_idx + ck_end, bytes(ck_data)
