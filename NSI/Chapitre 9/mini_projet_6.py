from random import randint
import sys

sys.setrecursionlimit(10000)

################## PARTIE 1 - ETAPE 2 ######################


def tri_bulle(liste: list):
    nb_permutation = 1
    while nb_permutation:
        nb_permutation = 0
        for i in range(len(liste) - 1):
            if liste[i] > liste[i + 1]:
                liste[i], liste[i + 1] = liste[i + 1], liste[i]
                nb_permutation += 1
    return liste


def test_tri_bulle():
    print("##### DEBUT TEST TRI BULLE #####")
    try:
        assert tri_bulle([1, 2, 3, 4, 5, 6, 7, 8, 9]) == [1, 2, 3, 4, 5, 6, 7, 8, 9], "Test 1"
        assert tri_bulle([9, 8, 7, 6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6, 7, 8, 9], "Test 2"
        assert tri_bulle([1, 1, 1, 1, 1, 1, 1, 1, 1]) == [1, 1, 1, 1, 1, 1, 1, 1, 1], "Test 3"

        l = list(range(1000, 0, -1))
        assert tri_bulle(l) == sorted(l), "Test 4"

        l = [randint(0, 1000) for _ in range(1000)]
        assert tri_bulle(l) == sorted(l), "Test 5"

        print("Succès des tests du tri bulle.")

    except AssertionError as error:
        print(f"Erreur dans les tests du tri bulle : {error}")

    except Exception as e:
        print(f"Une erreur s'est produite durant les tests : {e}")

    print("##### FIN TEST TRI BULLE #####\n")


def tri_bulle_optimise(liste: list):
    for i in range(len(liste), 0, -1):
        trie = True
        for j in range(i - 1):
            if liste[j] > liste[j + 1]:
                liste[j], liste[j + 1] = liste[j + 1], liste[j]
                trie = False
        if trie:
            return liste
    return liste


def test_tri_bulle_optimise():
    print("##### DEBUT TEST TRI BULLE OPTIMISE #####")
    try:
        assert tri_bulle_optimise([1, 2, 3, 4, 5, 6, 7, 8, 9]) == [1, 2, 3, 4, 5, 6, 7, 8, 9], "Test 1"
        assert tri_bulle_optimise([9, 8, 7, 6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6, 7, 8, 9], "Test 2"
        assert tri_bulle_optimise([1, 1, 1, 1, 1, 1, 1, 1, 1]) == [1, 1, 1, 1, 1, 1, 1, 1, 1], "Test 3"

        l = list(range(1000, 0, -1))
        assert tri_bulle_optimise(l) == sorted(l), "Test 4"

        l = [randint(0, 1000) for _ in range(1000)]
        assert tri_bulle_optimise(l) == sorted(l), "Test 5"

        print("Succès des tests du tri bulle optimisé.")

    except AssertionError as error:
        print(f"Erreur dans les tests du tri bulle optimisé: {error}")

    except Exception as e:
        print(f"Une erreur s'est produite durant les tests : {e}")

    print("##### FIN TEST TRI BULLE OPTIMISE #####\n")


################## PARTIE 1 - ETAPE 4 ######################


def tri_bulle_nb_iteration(liste: list):
    nb_permutation = 1
    nb_iterations = 0
    while nb_permutation:
        nb_permutation = 0
        for i in range(len(liste) - 1):
            nb_iterations += 1
            if liste[i] > liste[i + 1]:
                liste[i], liste[i + 1] = liste[i + 1], liste[i]
                nb_permutation += 1
    return nb_iterations


def afficher_nb_iteration_tri_bulle():
    print(tri_bulle_nb_iteration(list(range(10, 0, -1))))
    print(tri_bulle_nb_iteration(list(range(20, 0, -1))))
    print(tri_bulle_nb_iteration(list(range(50, 0, -1))))
    print(tri_bulle_nb_iteration(list(range(100, 0, -1))))
    print(tri_bulle_nb_iteration(list(range(500, 0, -1))))
    print(tri_bulle_nb_iteration(list(range(1000, 0, -1))))


################## PARTIE 2 - ETAPE 2 ######################


def tri_rapide(liste: list):
    if len(liste) <= 1:
        return liste

    pivot = liste[0]
    liste1 = []
    liste2 = []

    for elem in liste[1:]:
        if elem <= pivot:
            liste1.append(elem)
        else:
            liste2.append(elem)

    return tri_rapide(liste1) + [pivot] + tri_rapide(liste2)


def partitionner(l: list, premier: int, dernier: int, pivot: int):
    l[pivot], l[dernier] = l[dernier], l[pivot]
    j = premier
    for i in range(j, dernier):
        if l[i] <= l[dernier]:
            l[j], l[i] = l[i], l[j]
            j += 1
    l[j], l[dernier] = l[dernier], l[j]
    return j


def tri_rapide_en_place(l: list, premier: int = 0, dernier: int = -1):
    if dernier == -1:
        dernier = len(l) - 1

    if premier < dernier:
        pivot = choix_pivot(l, premier, dernier)
        pivot = partitionner(l, premier, dernier, pivot)
        tri_rapide_en_place(l, premier, pivot - 1)
        tri_rapide_en_place(l, pivot + 1, dernier)


def choix_pivot(l: list, premier: int, dernier: int):
    return randint(premier, dernier)


def test_tri_rapide():
    print("##### DEBUT TEST TRI RAPIDE #####")
    try:
        assert tri_rapide([1, 2, 3, 4, 5, 6, 7, 8, 9]) == [1, 2, 3, 4, 5, 6, 7, 8, 9], "Test 1"
        assert tri_rapide([9, 8, 7, 6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6, 7, 8, 9], "Test 2"
        assert tri_rapide([1, 1, 1, 1, 1, 1, 1, 1, 1]) == [1, 1, 1, 1, 1, 1, 1, 1, 1], "Test 3"

        l = list(range(1000, 0, -1))
        assert tri_rapide(l) == sorted(l), "Test 4"

        l = [randint(0, 1000) for _ in range(10000)]
        assert tri_rapide(l) == sorted(l), "Test 5"

        print("Succès des tests du tri rapide.")

    except AssertionError as error:
        print(f"Erreur dans les tests du tri rapide : {error}")

    except Exception as e:
        print(f"Une erreur s'est produite durant les tests : {e}")

    finally:
        print("##### FIN TEST TRI RAPIDE #####\n")


def test_tri_rapide_en_place():
    print("##### DEBUT TEST TRI RAPIDE EN PLACE #####")
    try:
        l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        l_sorted = sorted(l)
        tri_rapide_en_place(l)
        assert l == l_sorted, "Test 1"

        l = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        l_sorted = sorted(l)
        tri_rapide_en_place(l)
        assert l == l_sorted, "Test 2"

        l = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        l_sorted = sorted(l)
        tri_rapide_en_place(l)
        assert l == l_sorted, "Test 3"

        l = list(range(10000, 0, -1))
        l_sorted = sorted(l)
        tri_rapide_en_place(l)
        assert l == l_sorted, "Test 4"

        l = [randint(0, 1000) for _ in range(10000)]
        l_sorted = sorted(l)
        tri_rapide_en_place(l)
        assert l == l_sorted, "Test 5"

        print("Succès des tests du tri rapide en place.")

    except AssertionError as error:
        print(f"Erreur dans les tests du tri rapide en place: {error}")

    except Exception as e:
        print(f"Une erreur s'est produite durant les tests : {e}")

    print("##### FIN TEST TRI RAPIDE EN PLACE #####\n")


################## PARTIE 2 - ETAPE 3 ######################

import matplotlib.pyplot as plt
from insertion import tri_insertion
from selection import tri_selection
from tri_ABR import tri_par_ABR
from fusion import tri_fusion
from temps import temps_execution


def liste_image(tri, liste_abs):
    """Fonction qui renvoie une liste de temps d'exécution pour un tri donné"""
    liste = []
    for taille in liste_abs:
        somme = sum(temps_execution(tri, taille) for _ in range(10))
        moyenne = somme / 10
        liste.append(moyenne)
    return liste


def afficher_courbes():
    liste_abs = [200 * n for n in range(1, 6)]

    plt.scatter(liste_abs, liste_image(tri_insertion, liste_abs), color="blue")
    plt.scatter(liste_abs, liste_image(tri_selection, liste_abs), color="red")
    plt.scatter(liste_abs, liste_image(tri_par_ABR, liste_abs), color="green")
    plt.scatter(liste_abs, liste_image(tri_fusion, liste_abs), color="orange")
    plt.scatter(liste_abs, liste_image(sorted, liste_abs), color="purple")
    plt.scatter(liste_abs, liste_image(tri_bulle, liste_abs), color="brown")
    plt.scatter(liste_abs, liste_image(tri_rapide, liste_abs), color="black")
    plt.show()

    # Une analyse des différents tri est disponible dans le document .odt


################## PARTIE 2 - ETAPE 4 ######################


def tri_rapide_pivot_aleatoire(liste: list):
    if len(liste) <= 1:
        return liste

    i_pivot = randint(0, len(liste) - 1)
    l = liste.copy()
    pivot = l.pop(i_pivot)

    liste1 = []
    liste2 = []

    for elem in l:
        if elem <= pivot:
            liste1.append(elem)
        else:
            liste2.append(elem)

    return tri_rapide_pivot_aleatoire(liste1) + [pivot] + tri_rapide_pivot_aleatoire(liste2)


def test_tri_rapide_pivot_aleatoire():
    print("##### DEBUT TEST TRI RAPIDE A PIVOT ALEATOIRE #####")
    try:
        assert tri_rapide_pivot_aleatoire([1, 2, 3, 4, 5, 6, 7, 8, 9]) == [1, 2, 3, 4, 5, 6, 7, 8, 9], "Test 1"
        assert tri_rapide_pivot_aleatoire([9, 8, 7, 6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6, 7, 8, 9], "Test 2"
        assert tri_rapide_pivot_aleatoire([1, 1, 1, 1, 1, 1, 1, 1, 1]) == [1, 1, 1, 1, 1, 1, 1, 1, 1], "Test 3"

        l = list(range(10000, 0, -1))
        assert tri_rapide_pivot_aleatoire(l) == sorted(l), "Test 4"

        l = [randint(0, 1000) for _ in range(10000)]
        assert tri_rapide_pivot_aleatoire(l) == sorted(l), "Test 5"

        print("Succès des tests du tri rapide à pivot aléatoire.")

    except AssertionError as error:
        print(f"Erreur dans les tests du tri rapide à pivot aléatoire: {error}")

    except Exception as e:
        print(f"Une erreur s'est produite durant les tests : {e}")

    print("##### FIN TEST TRI RAPIDE A PIVOT ALEATOIRE #####\n")


################## MAIN ######################


def main():
    test_tri_bulle()  # PARTIE 1 - ETAPE 2
    test_tri_bulle_optimise()  # NON DEMANDE

    # afficher_nb_iteration_tri_bulle()  # PARTIE 1 - ETAPE 4

    test_tri_rapide()  # PARTIE 2 - ETAPE 2
    test_tri_rapide_en_place()  # PARTIE 2 - ETAPE 2

    test_tri_rapide_pivot_aleatoire()  # PARTIE 2 - ETAPE 4

    afficher_courbes()  # PARTIE 2 - ETAPE 3


if __name__ == "__main__":
    main()
