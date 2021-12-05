from abr import ABR
from parcours import infixe


def bien_construit(arbre):
    """fonction qui teste si un ABR est bien construit"""
    if arbre is None:
        return False
    h = arbre.hauteur()
    return (2 ** (h - 1)) <= arbre.taille() <= (2 ** h - 1)


def tri_par_ABR(liste):
    abr = ABR(liste[0])
    for elem in liste[1:]:
        abr.inserer(elem)

    return infixe(abr)


print(tri_par_ABR([1, 7, 9, 3]))
print(tri_par_ABR([9, 5, 1, 7, 3, 4, 6, 8, 2]))
