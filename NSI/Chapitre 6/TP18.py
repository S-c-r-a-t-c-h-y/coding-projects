from arbre_binaire import AB
from file import File
from dessiner_arbre import dessiner


def largeur(arbre):
    """Fonction qui retourne le parcours en largeur de l'arbre
    sous la forme d'une liste
    """
    liste = []
    if arbre != None:
        f1 = File()
        f1.enfiler(arbre)
        while f1.est_vide() == False:
            a = f1.defiler()
            liste.append(a.get_val())
            if a.get_ag() is not None:
                f1.enfiler(a.get_ag())
            if a.get_ad() is not None:
                f1.enfiler(a.get_ad())
    return liste


def est_parfait(arbre):
    return arbre.taille() == (2 ** arbre.hauteur() - 1) if arbre is not None else False


arbre1 = AB(2, AB(3), AB(8))
arbre2 = AB(8, AB(5, AB(1), AB(2)), AB(7))
arbre3 = AB(5, AB(4, AB(2), AB(3)), AB(8, AB(9), AB(1)))

dessiner(arbre1)
print(largeur(arbre1))
print(est_parfait(arbre1))

dessiner(arbre2)
print(largeur(arbre2))
print(est_parfait(arbre2))

dessiner(arbre3)
print(largeur(arbre3))
print(est_parfait(arbre3))
