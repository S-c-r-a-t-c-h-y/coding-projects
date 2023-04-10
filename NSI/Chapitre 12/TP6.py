def maximum1(liste):
    if not liste:
        return None
    maximum = liste[0]
    for elem in liste:
        if elem > maximum:
            maximum = elem
    return maximum


def maximum2(liste):
    if not liste:
        return None
    if len(liste) == 1:
        return liste[0]
    max1 = maximum2(liste[: len(liste) // 2])
    max2 = maximum2(liste[len(liste) // 2 :])
    if max1 > max2:
        return max1
    return max2


def test():
    liste1 = [-2, 5, 1, -8, 14, 7, 6, -3, 0, 9]
    liste2 = [i % 30 for i in range(100)]
    liste3 = []
    print("maximum1 :", maximum2(liste1))
    print("maximum2 :", maximum2(liste2))
    print("maximum3 :", maximum2(liste3))


if __name__ == "__main__":
    test()
