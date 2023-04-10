from time import time
from random import randint
from selection import tri_selection


def temps_execution(tri, taille):
    """ " Fonction qui calcule le temps d'exécution d'un tri"""
    somme = 0
    for _ in range(10):
        liste1 = [randint(0, 2 * taille) for _ in range(taille)]
        t1 = time()
        tri(liste1)
        t2 = time()
        somme += t2 - t1
    return somme / 10


taille = int(input("Saisir la taille de la liste : "))
print(f"temps d'execution : {temps_execution(tri_selection, taille):.4f}")
