from time import time
from random import randint
from insertion import tri_insertion


def temps_execution(tri, taille):
    """ " Fonction qui calcule le temps d'exécution d'un tri"""
    liste1 = [randint(0, 2 * taille) for _ in range(taille)]
    t1 = time()
    tri(liste1)
    t2 = time()
    return t2 - t1


taille = int(input("Saisir la taille de la liste : "))
print(f"temps d'execution : {temps_execution(tri_insertion, taille):.4f}")
