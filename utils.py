"""
Utils
"""
import numpy as np


def unpack_elem(elem, n_bits):
    return np.array(
        [elem & (0x01 << i) for i in range(n_bits)[::-1]], dtype=np.bool
    )

def pack_bits(bits):
    n_bits = len(bits)
    mask = np.logspace(n_bits-1, 0, n_bits, base=2, dtype=np.int64)
    return (bits * mask).sum()


def unpack_arr(arr, n_bits):
    unpacked_arr = np.zeros([len(arr), n_bits], dtype=np.bool)
    mask = [0x01 << i for i in range(n_bits)[::-1]]
    for i, elem in enumerate(arr):
        unpacked_arr[i] = np.array([elem & j for j in mask], dtype=np.bool)
    return unpacked_arr

def pack_arr(arr):
    n_bits = arr.shape[1]
    packed_arr = np.zeros([len(arr)], dtype=np.int64)
    mask = np.logspace(n_bits-1, 0, n_bits, base=2, dtype=np.int64)
    for i, elem in enumerate(arr):
        packed_arr[i] = (elem * mask).sum()
    return packed_arr


def get_all_unpacked_bits(n_bits):
    """Get an unpacked binary matrix of n bits
    """
    return unpack_arr(range(2**n_bits), n_bits)


if __name__ == "__main__":
    #print(pack_bits(unpack_elem(0, 8)))
    #print(pack_bits(unpack_elem(1, 8)))
    #print(pack_bits(unpack_elem(254, 8)))
    print(pack_arr(unpack_arr(np.array([0, 1, 253]), 8)))
    #print(get_all_unpacked_bits(8))
