from abr import *


def successeur(abr):
    """Fonction qui retourne le successeur de la racine de l'abr"""

    if abr is not None:
        abr1 = abr.get_ad()

        while abr1.get_ag() != None:
            abr1 = abr1.get_ag()

        return abr1.get_val()


def supprimer(abr, val):
    """Fonction qui supprime le noeud dont la clé est val dans
    l'arbre binaire de recherche abr"""

    if abr is None or val not in abr:
        return abr

    new_abr = abr
    pere = None

    while (cur_val := new_abr.get_val()) != val:
        pere = new_abr
        new_abr = new_abr.get_ad() if val >= cur_val else new_abr.get_ag()

    if new_abr.get_ad() is None and new_abr.get_ag() is None:
        if val < pere.get_val():
            pere.set_ag(None)
        else:
            pere.set_ad(None)

    elif new_abr.get_ad() is not None and new_abr.get_ag() is not None:
        succ = successeur(new_abr)
        supprimer(new_abr, succ)
        new_abr.set_val(succ)

    else:
        fils = new_abr.get_ad() if new_abr.get_ad() is not None else new_abr.get_ag()
        if val < pere.get_val():
            pere.set_ag(fils)
        else:
            pere.set_ad(fils)

    return abr


abr1 = ABR(4)
abr1.inserer(2)
abr1.inserer(1)
abr1.inserer(3)
abr1.inserer(6)
abr1.inserer(5)
abr1.inserer(7)
abr1.inserer(9)
abr1.inserer(8)

dessiner(abr1)
supprimer(abr1, 8)
dessiner(abr1)

print("---------------------------------")

abr1 = ABR(4)
abr1.inserer(2)
abr1.inserer(1)
abr1.inserer(3)
abr1.inserer(6)
abr1.inserer(5)
abr1.inserer(7)
abr1.inserer(9)
abr1.inserer(8)

dessiner(abr1)
supprimer(abr1, 6)
dessiner(abr1)
