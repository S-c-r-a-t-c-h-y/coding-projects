from abr import *


def cle_max(abr):
    """fonction qui retourne la valeur maximale contenu dans un abr"""
    if abr != None:
        abr1 = abr
        while abr1.get_ad() != None:
            abr1 = abr1.get_ad()
        return abr1.get_val()


abr1 = ABR(4)
abr1.inserer(2)
abr1.inserer(1)
abr1.inserer(3)
abr1.inserer(6)
abr1.inserer(5)
abr1.inserer(7)

abr2 = ABR(4)
abr2.inserer(2)
abr2.inserer(1)

abr3 = ABR(8)
abr3.inserer(10)
abr3.inserer(2)
abr3.inserer(15)
abr3.inserer(7)
abr3.inserer(6)

dessiner(abr1)
print(cle_max(abr1))

dessiner(abr2)
print(cle_max(abr2))

dessiner(abr3)
print(cle_max(abr3))
