from file import *
from dessiner_graphe import *

G = {
    "A": ["B", "C", "D"],
    "B": ["A", "C", "E"],
    "C": ["A", "B", "E", "F"],
    "D": ["A", "F"],
    "E": ["B", "C", "F"],
    "F": ["C", "D", "E"],
}


def parcours_largeur(G, s):
    etat = {s: 0 for s in G}
    liste = []
    file = File()
    file.enfiler(s)
    etat[s] = 1
    while not file.est_vide():
        s = file.defiler()
        liste.append(s)
        for a in G[s]:
            if etat[a] == 0:
                file.enfiler(a)
                etat[a] = 1
    return liste


print(parcours_largeur(G, "A"))
print(parcours_largeur(G, "F"))
