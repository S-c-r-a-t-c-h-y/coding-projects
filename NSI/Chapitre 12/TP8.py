def puissance1(x, n):
    if n == 0:
        return 1
    puissance = x
    for _ in range(n - 1):
        puissance *= x
    return puissance


def puissance2(x, n):
    if n == 0:
        return 1
    if n % 2:
        return x * puissance2(x, n - 1)
    p = puissance2(x, n // 2)
    return p * p


def test():
    print("puissance1 :", puissance2(2, 8))
    print("puissance2 :", puissance2(10, 3))
    print("puissance3 :", puissance2(-3, 7))
    print("puissance4 :", puissance2(5, 0))


if __name__ == "__main__":
    test()
