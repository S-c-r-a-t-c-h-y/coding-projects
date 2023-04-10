from arbre_binaire import AB
from dessiner_arbre import dessiner


def hauteur(arbre):
    """Fonction qui renvoie la hauteur d'un arbre binaire"""
    # si l'arbre est vide

    if arbre is None:
        return 0

    hg = hauteur(arbre.get_ag())
    hd = hauteur(arbre.get_ad())
    return max(hg, hd) + 1


def taille(arbre):
    """Fonction qui renvoie la taille d'un arbre binaire"""

    if arbre is None:
        return 0

    tg = taille(arbre.get_ag())
    td = taille(arbre.get_ad())

    return tg + td + 1


def contient(valeur, arbre):
    if arbre is None:
        return False
    if arbre.get_val() == valeur:
        return True
    return any((contient(valeur, arbre.get_ag()), contient(valeur, arbre.get_ad())))


arbre3 = AB(1, AB(2, AB(4, AB(5), AB(6))))

print(contient(3, arbre3))
print(contient(5, arbre3))
print(contient(6, arbre3))
print(contient(0, arbre3))
