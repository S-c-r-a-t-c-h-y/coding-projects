from abr import *


def successeur(abr):
    """Fonction qui retourne le successeur de la racine de l'abr"""

    if abr is not None:
        abr1 = abr.get_ad()

        while abr1.get_ag() != None:
            abr1 = abr1.get_ag()

        return abr1.get_val()


abr1 = ABR(4)
abr1.inserer(2)
abr1.inserer(1)
abr1.inserer(3)
abr1.inserer(6)
abr1.inserer(5)
abr1.inserer(7)
abr1.inserer(9)
abr1.inserer(8)

abr2 = ABR(7)
abr2.inserer(5)
abr2.inserer(9)
abr2.inserer(8)
abr2.inserer(1)

dessiner(abr1)
print(successeur(abr1))

dessiner(abr2)
print(successeur(abr2))
