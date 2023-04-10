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


def test():
    liste1 = list(range(500))
    print("recherche1 :", rechercher2(4080, liste1))
    print("recherche2 :", rechercher2(450, liste1))


if __name__ == "__main__":
    test()
