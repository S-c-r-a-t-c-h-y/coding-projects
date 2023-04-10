import matplotlib.pyplot as plt
from insertion import tri_insertion
from selection import tri_selection
from tri_ABR import tri_par_ABR
from fusion import tri_fusion
from temps import temps_execution

liste_abs = [200 * n for n in range(1, 11)]
liste_abs.extend([3000, 4000, 5000])

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


plt.title("Comparaison temps d'execution des différents tris")
plt.ylabel("temps d'execution (en s)")
plt.xlabel("nombres d'éléments de la liste")
plt.yscale("log")
plt.plot(liste_abs, liste_image(tri_insertion), color="blue", label="tri par insertion")
plt.plot(liste_abs, liste_image(tri_selection), color="red", label="tri par selection")
plt.plot(liste_abs, liste_image(tri_par_ABR), color="green", label="tri rapide")
plt.plot(liste_abs, liste_image(tri_fusion), color="orange", label="tri fusion")
plt.plot(liste_abs, liste_image(sorted), color="purple", label="List.sort Ocaml")
plt.legend()
plt.show()
