def RechercheMin(tab):
    """Fonction qui renvoi l'indice tu minimum du tableau tab

    :param tab: de type list
    :param tab: éléments de type int ou float
    :return: de type int
    """

    # Test des préconditions
    assert isinstance(tab, list), "Le premier paramètre doit être de type list."
    for nombre in tab:
        assert isinstance(nombre, (int, float)), "Les éléments de tab doivent être des nombres."

    # Code de la fonction
    if not tab:  # la liste est vide, il n'y a pas de minimum
        return None
    indice = 0
    for i in range(len(tab)):
        if tab[i] < tab[indice]:
            indice = i
    return indice


def test1():
    print("-" * 60)
    print("RechercheMin([5]) :")
    print(RechercheMin([5]))
    print("-" * 60)
    print("RechercheMin([2, 4, 1]) :")
    print(RechercheMin([2, 4, 1]))
    print("-" * 60)
    print("RechercheMin([5, 3, 2, 2, 4]) :")
    print(RechercheMin([5, 3, 2, 2, 4]))
    print("-" * 60)
    print("RechercheMin([5, 3, 2, '2', 4]) :")
    print(RechercheMin([5, 3, 2, "2", 4]))
    print("-" * 60)


def separe(tab):
    """Fonction qui sépare les 0 et les 1 du tableau tab

    :param tab: de type list
    :param tab: éléments égaux à 0 ou 1
    :return: de type list
    """
    # Test des préconditions
    assert isinstance(tab, list), "Le premier paramètre doit être de type list."
    for element in tab:
        assert element in [0, 1], "Les éléments de tab doivent être égaux à 0 ou 1."

    # Code de la fonction
    i = 0
    j = len(tab) - 1
    while i < j:
        if tab[i] == 0:
            i += 1
        else:
            tab[i], tab[j] = tab[j], tab[i]
            j -= 1
    return tab


def test2():
    print("-" * 60)
    print("separe([1, 0, 1, 0, 1, 0, 1, 0]) :")
    print(separe([1, 0, 1, 0, 1, 0, 1, 0]))
    print("-" * 60)
    print("separe([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0]) :")
    print(separe([1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0]))
    print("-" * 60)
    print("separe([1, 0, 0, 0, 1, 1, 0, 2, 1, 0, 1, 0, 1, 1, 1, 0]) :")
    print(separe([1, 0, 0, 0, 1, 1, 0, 2, 1, 0, 1, 0, 1, 1, 1, 0]))
    print("-" * 60)


if __name__ == "__main__":
    # test1()
    test2()
