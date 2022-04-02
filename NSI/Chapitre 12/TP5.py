def maximum1(liste):
    if not liste:
        return None
    maximum = liste[0]
    for elem in liste:
        if elem > maximum:
            maximum = elem
    return maximum


def test():
    liste1 = [-2, 5, 1, -8, 14, 7, 6, -3, 0, 9]
    liste2 = [i % 20 for i in range(50)]
    liste3 = []
    print("maximum1 :", maximum1(liste1))
    print("maximum2 :", maximum1(liste2))
    print("maximum3 :", maximum1(liste3))


if __name__ == "__main__":
    test()
