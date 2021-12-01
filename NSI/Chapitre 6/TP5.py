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


arbre1 = None
arbre2 = AB(1, AB(3), AB(2))
arbre3 = AB(1, AB(2), AB(2, AB(4)))
arbre4 = AB(1)
arbre5 = AB(1, AB(2))

print(hauteur(arbre1))
print(hauteur(arbre2))
print(hauteur(arbre3))
print(hauteur(arbre4))
print(hauteur(arbre5))
