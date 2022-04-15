from math import sqrt  # import de la fonction racine carree


def recherche(tab, n):
    """Renvoi l'indice de la dernière occurence de n dans tab si
    n est dans tab et la longueur de tab dans le cas contraire.

    :param tab: tableau non vide d'entier de type list
    :param n: nombre entier
    :return: nombre de type int
    """
    ### Test des préconditions ###
    assert len(tab), "Le tableau ne doit pas être vide."
    assert isinstance(tab, list), "Le tableau doit être de type list."
    assert isinstance(n, int), "Le nombre recherché doit être de type int."
    for entier in tab:
        assert isinstance(entier, int), "Les éléments du tableau doivent être des entiers."

    ### Code de la fonction ###
    indice = -1
    for i in range(len(tab)):
        if tab[i] == n:
            indice = i
    return indice if indice != -1 else len(tab)


def test1():
    assert recherche([5, 3], 1) == 2
    assert recherche([2, 4], 2) == 0
    assert recherche([2, 3, 5, 2, 4], 2) == 3


def distance(point1, point2):
    """Calcule et renvoie la distance entre deux points."""
    return sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def plus_courte_distance(tab, depart):
    """Renvoie le point du tableau tab se trouvant a la plus
    courte distance du point depart.

    :param tab: tableau contenant des couples d'entiers sous forme de tuple représentant les coordonnées de points
    :param depart: couple d'entier représentant les coordonnées du point de départ.
    :return: couple d'entier représentant les coordonnées du point le plus proche du départ.
    """
    ### Test des préconditions ###
    assert isinstance(tab, list), "Le tableau doit être de type list."
    assert isinstance(depart, tuple), "Le point de départ doit être de type tuple."
    assert isinstance(depart[0], int) and isinstance(depart[1], int), "Les coordonnées du point de départ doivent être entières."
    for point in tab:
        assert isinstance(point, tuple), "Les éléments du tableau doivent être de type tuple."
        assert isinstance(point[0], int) and isinstance(point[1], int), "Les coordonnées des points de tab doivent être entières."

    ### Code de la fonction ###
    point = tab[0]
    min_dist = distance(depart, point)
    for i in range(1, len(tab)):
        if distance(tab[i], depart) < min_dist:
            point = tab[i]
            min_dist = distance(tab[i], depart)
    return point


def test2():
    assert distance((1, 0), (5, 3)) == 5.0, "erreur de calcul"
    assert plus_courte_distance([(7, 9), (2, 5), (5, 2)], (0, 0)) == (2, 5), "erreur"


if __name__ == "__main__":
    test1()
    test2()
