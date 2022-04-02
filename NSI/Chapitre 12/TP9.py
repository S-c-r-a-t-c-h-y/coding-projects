from time import perf_counter
from random import randint


# def multiplication(n1, n2):
#     n = len(str(n1))
#     if n <= 1:
#         return n1 * n2
#     k = n // 2

#     a = n1 // 10 ** k
#     b = n1 % 10 ** k
#     c = n2 // 10 ** k
#     d = n2 % 10 ** k

#     a0 = multiplication(a, c)
#     a1 = multiplication(a + b, c + d)
#     a2 = multiplication(b, d)

#     return a0 * 100 ** k + (a1 - a0 - a2) * 10 ** k + a2


def multiplication(n1, n2):
    n = len(str(n1))
    if n == 1:
        return n1 * n2
    k = n // 2

    a = int(str(n1).rjust(n, "0")[:k])
    b = int(str(n1).rjust(n, "0")[k:])
    c = int(str(n2).rjust(n, "0")[:k])
    d = int(str(n2).rjust(n, "0")[k:])

    a0 = multiplication(a, c)
    ab = a - b
    cd = c - d
    if ab < 0 and cd < 0:
        a1 = multiplication(abs(ab), abs(cd))
    elif ab < 0 or cd < 0:
        a1 = -multiplication(abs(ab), abs(cd))
    else:
        a1 = multiplication(ab, cd)
    a2 = multiplication(b, d)

    return a0 * 100 ** k + (a0 + a2 - a1) * 10 ** k + a2


def test():
    print("multiplication1 :", multiplication(48, 12))
    print("multiplication2 :", multiplication(1014, 3875))
    print("multiplication3 :", multiplication(45087158, 15975347))


def perf_test():
    n1 = randint(10 ** 63, 10 ** 64)
    n2 = randint(10 ** 63, 10 ** 64)

    t1 = perf_counter()
    r1 = multiplication(n1, n2)
    t2 = perf_counter()
    p1 = t2 - t1
    print(p1, r1)

    t3 = perf_counter()
    r2 = n1 * n2
    t4 = perf_counter()
    p2 = t4 - t3
    print(p2, r2)

    print(p1 / p2)


if __name__ == "__main__":
    test()
    perf_test()
