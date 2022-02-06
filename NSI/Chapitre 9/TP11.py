from time import time
from random import randint
import matplotlib.pyplot as plt
from insertion import tri_insertion
from selection import tri_selection
from temps import temps_execution

liste_abs = [200 * n for n in range(1, 14)]


def liste_image(tri):
    """Fonction qui renvoie une liste de temps d'exécution pour un tri donné"""
    liste = []
    for taille in liste_abs:
        somme = 0
        for i in range(10):
            somme += temps_execution(tri, taille)
        moyenne = somme / 10
        liste.append(moyenne)
    return liste


plt.scatter(liste_abs, liste_image(tri_insertion), color="blue")
plt.scatter(liste_abs, liste_image(tri_selection), color="red")
plt.show()
