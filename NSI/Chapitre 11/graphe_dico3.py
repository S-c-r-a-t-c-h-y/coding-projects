from pile import *
from dessiner_graphe import *


G = {
    "A": ["B", "C", "D"],
    "B": ["A", "E", "F"],
    "C": ["A", "G"],
    "D": ["A"],
    "E": ["B"],
    "F": ["B"],
    "G": ["C"],
}


def parcours_profondeur_2(G, s):
    etat = {s: 0 for s in G}
    liste = [s]
    pile = Pile()
    pile.empiler(s)
    etat[s] = 1
    while not pile.est_vide():
        s = pile.sommet()
        if liste_adjacents_non_visite := [a for a in G[s] if etat[a] == 0]:
            a1 = liste_adjacents_non_visite[0]
            liste.append(a1)
            pile.empiler(a1)
            etat[a1] = 1
        else:
            pile.depiler()
    return liste


print(parcours_profondeur_2(G, "A"))
print(parcours_profondeur_2(G, "G"))
dessiner1(G)
