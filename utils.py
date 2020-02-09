"""Utils
Pack binary bits into scales and reverse.
"""
import numpy as np


def unpack_scale(elem, n_bits):
    """Unpack a scale to an array of bits

    Args:
        scale: A integer to unopack.
        n_bits: Width of bits.
    
    Returns:
        A boolean numpy array of unpacked bits of size [n_bits].
        Each element a_i represents 2^(n_bits-1-i).
        For example:

        scale = 5, n_bits = 4
        5 = 0*2^3 + 1*2^2 + 0*2^1 + 1*2^0
        return np.array([False, True, False, True], dtype=np.bool)
    """
    return np.array(
        [elem & (0x01 << i) for i in range(n_bits)[::-1]], dtype=np.bool
    )


def pack_bits(bits):
    """Pack an array of bits to a scale. Inverse of unpack_scale
    """
    n_bits = len(bits)
    mask = np.logspace(n_bits-1, 0, n_bits, base=2, dtype=np.int64)
    return (bits * mask).sum()


def unpack_arr_scale(arr, n_bits):
    """Unpack all scales in the array to bits

    Args:
        arr: A numpy array of integers to unpack.
        n_bits: Width of bits.

    Returns:
        A boolean 2-d numpy array of unpacked bits of size [len(arr), n_bits].
        For example:

        arr = [1, 5], n_bits = 4
        return np.array([
            [False, False, False, True], # 1
            [False, True, False, True], # 5
        ])
    """
    unpacked_arr = np.zeros([len(arr), n_bits], dtype=np.bool)
    mask = [0x01 << i for i in range(n_bits)[::-1]]
    for i, elem in enumerate(arr):
        unpacked_arr[i] = np.array([elem & j for j in mask], dtype=np.bool)
    return unpacked_arr


def pack_arr_bits(arr):
    """Pack a 2-d array of bits to a 1-d array of scales. Inverse of unpack_arr_scale
    """
    n_bits = arr.shape[1]
    packed_arr = np.zeros([len(arr)], dtype=np.int64)
    mask = np.logspace(n_bits-1, 0, n_bits, base=2, dtype=np.int64)
    for i, elem in enumerate(arr):
        packed_arr[i] = (elem * mask).sum()
    return packed_arr


def get_all_unpacked_bits(n_bits):
    """Get all unpacked bits of width n_bits.

    Args:
        n_bits: Width.

    Returns:
        A boolean 2-d numpy array of size [2^n_bits, n_bits]
    """
    return unpack_arr_scale(range(2**n_bits), n_bits)


if __name__ == "__main__":
    #print(pack_bits(unpack_elem(0, 8)))
    #print(pack_bits(unpack_elem(1, 8)))
    #print(pack_bits(unpack_elem(254, 8)))
    print(pack_arr_bits(unpack_arr_scale(np.array([0, 1, 253]), 8)))
    # print(get_all_unpacked_bits(8))
