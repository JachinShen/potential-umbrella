import numpy as np


def pad101(x, m):
    j = (-m-2) % x
    return "1{}1".format("".join(["0"]*j))


def keccak(msg, c=448, d=224):
    msg += "01"
    r = int(1600 - c)
    apd_msg = pad101(len(msg), r)
    msg += apd_msg
    print(msg)


def SHA3_224(msg):
    return keccak(msg)


def A2Str(A):
    tmp = sum([A[:, :, z] << z for z in range(64)])
    for y in range(5):
        for x in range(5):
            v = tmp[x, y]
            for i in range(8):
                print("{:02X}".format(v & 0xFF), end=" ")
                v >>= 8
    print("")


def main():
    # SHA3_224("11001")
    A = np.zeros([5, 5, 64], dtype=np.bool)
    A[0, 0, 1] = True
    A[0, 0, 2] = True
    A2Str(A)

    # Theta
    C = A[:, 0] ^ A[:, 1] ^ A[:, 2] ^ A[:, 3] ^ A[:, 4]
    D = np.zeros_like(C)
    # D = C[[4, 0, 1, 2, 3]]
    for x in range(5):
        for z in range(64):
            D[x, z] = C[(x-1) % 5, z] ^ C[(x+1) % 5, (z-1) % 5]
    for y in range(5):
        A[:, y] ^= D
    A2Str(A)


if __name__ == "__main__":
    main()
