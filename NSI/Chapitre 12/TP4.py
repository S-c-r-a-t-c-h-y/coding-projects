def rechercher1(e, liste):
    for elem in liste:
        if elem == e:
            return True
    return False


def rechercher2(e, liste):
    if not liste:
        return False
    m = liste[len(liste) // 2]
    if m == e:
        return True
    if m > e:
        return rechercher2(e, liste[: len(liste) // 2])
    return rechercher2(e, liste[len(liste) // 2 + 1 :])


def rechercher3(e, liste):
    i1 = 0
    i2 = len(liste) - 1
    im = (i1 + i2) // 2
    while i1 <= i2:
        if liste[im] == e:
            return True
        elif liste[im] > e:
            i2 = im - 1
        else:
            i1 = im + 1
        im = (i1 + i2) // 2
    return False


def test():
    liste1 = list(range(-200, 200))
    print("recherche1 :", rechercher3(-380, liste1))
    print("recherche2 :", rechercher3(150, liste1))
    print("recherche2 :", rechercher3(450, liste1))


if __name__ == "__main__":
    test()
