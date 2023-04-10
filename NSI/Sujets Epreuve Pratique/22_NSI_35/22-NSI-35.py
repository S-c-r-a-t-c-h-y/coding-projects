def moyenne(tab):
    """
    moyenne(list) -> float
    Entrée : un tableau non vide d'entiers
    Sortie : nombre de type float
    Correspondant à la moyenne des valeurs présentes dans le
    tableau
    """
    # Test des préconditions
    assert isinstance(tab, list), "Le tableau doit être de type list."
    assert len(tab), "Le tableau ne doit pas être vide."
    for entier in tab:
        assert isinstance(entier, int), "Les éléments du tableau doivent être des entiers."

    # Code de la fonction
    somme = 0
    for entier in tab:
        somme += entier
    return somme / len(tab)


def test1():
    assert moyenne([1]) == 1
    assert moyenne([1, 2, 3, 4, 5, 6, 7]) == 4
    assert moyenne([1, 2]) == 1.5


def dichotomie(tab, x):
    """
    tab : tableau trie dans l'ordre croissant
    x : nombre entier
    La fonction renvoie True si tab contient x et False sinon
    """
    ### Test des préconditions ###
    assert isinstance(x, int), "L'élément recherché doit être de type int."
    assert isinstance(tab, list), "Le tableau doit être de type list."
    for entier in tab:
        assert isinstance(entier, int), "Les éléments du tableau doivent être des entiers."

    ### Code de la fonction ###

    # cas du tableau vide
    if not len(tab):
        return False, 1

    # cas ou x n'est pas compris entre les valeurs extremes
    if (x < tab[0]) or (x > tab[-1]):
        return False, 2

    debut = 0
    fin = len(tab) - 1
    while debut <= fin:
        m = (debut + fin) // 2
        if x == tab[m]:
            return True
        if x > tab[m]:
            debut = m + 1
        else:
            fin = m - 1
    return False, 3


def test2():
    assert dichotomie([15, 16, 18, 19, 23, 24, 28, 29, 31, 33], 28) is True
    dichotomie([15, 16, 18, 19, 23, 24, 28, 29, 31, 33], 27) == (False, 3)
    dichotomie([15, 16, 18, 19, 23, 24, 28, 29, 31, 33], 1) == (False, 2)
    dichotomie([], 28) == (False, 1)


if __name__ == "__main__":
    test1()
    test2()
