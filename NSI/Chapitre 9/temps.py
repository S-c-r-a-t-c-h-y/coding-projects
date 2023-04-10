from time import time
from random import randint


def temps_execution(tri, taille):
    """ " Fonction qui calcule le temps d'exécution d'un tri"""
    liste1 = [randint(0, 2 * taille) for _ in range(taille)]
    t1 = time()
    tri(liste1)
    t2 = time()
    return t2 - t1
