def puissance1(x, n):
    if n == 0:
        return 1
    puissance = x
    for _ in range(n - 1):
        puissance *= x
    return puissance


def test():
    print("puissance1 :", puissance1(2, 10))
    print("puissance2 :", puissance1(10, 6))
    print("puissance3 :", puissance1(-3, 5))
    print("puissance4 :", puissance1(7, 0))


if __name__ == "__main__":
    test()
