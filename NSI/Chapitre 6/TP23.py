from abr import *


def bien_construit(arbre):
    """fonction qui teste si un ABR est bien construit"""
    if arbre is None:
        return False
    h = arbre.hauteur()
    return (2 ** (h - 1)) <= arbre.taille() <= (2 ** h - 1)


# abr1 : un abr bien construit
abr1 = ABR(4)
abr1.inserer(2)
abr1.inserer(1)
abr1.inserer(3)
abr1.inserer(6)
abr1.inserer(5)
abr1.inserer(7)

# abr2 : un abr pas bien construit
abr2 = ABR(4)
abr2.inserer(2)
abr2.inserer(1)

dessiner(abr1)
print(bien_construit(abr1))

dessiner(abr2)
print(bien_construit(abr2))
