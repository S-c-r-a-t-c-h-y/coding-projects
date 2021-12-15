from arbre_binaire import AB
from abr import ABR
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


def est_un_ABR(arbre):
    if arbre is None:
        return False

    ag = arbre.get_ag()
    ad = arbre.get_ad()

    if ag is not None and ad is not None:
        if not (ag.get_val() <= arbre.get_val() <= ad.get_val()):
            return False
        return all((est_un_ABR(ag), est_un_ABR(ad)))

    if ag is None and ad is not None:
        if ad.get_val() < arbre.get_val():
            return False
        return est_un_ABR(ad)

    if ad is None and ag is not None:
        if ag.get_val() > arbre.get_val():
            return False
        return est_un_ABR(ag)

    return True


arbre1 = AB(5, AB(4, AB(2), AB(3)), AB(8, AB(9), AB(1)))
arbre2 = AB(8, AB(5, AB(2), AB(6)), AB(12, AB(10), AB(14)))

arbre3 = AB(8, AB(4, AB(1), AB(6, None, AB(9))), AB(15, AB(11), AB(20)))

dessiner(arbre1)
print(est_un_ABR(arbre1))

dessiner(arbre2)
print(est_un_ABR(arbre2))

# dessiner(arbre3)
# print(est_un_ABR(arbre3))
