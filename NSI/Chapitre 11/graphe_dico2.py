from dessiner_graphe import *

G = {
    "A": ["C", "B", "D"],
    "B": ["A", "D", "E"],
    "C": ["A", "C", "D", "F"],
    "D": ["A", "B", "C", "E"],
    "E": ["B", "D", "F", "G"],
    "F": ["C", "E", "G"],
    "G": ["E", "F"],
}

dessiner1(G)


def parcours_profondeur(G, s, liste):
    liste.append(s)
    for sommet in G[s]:
        if sommet not in liste:
            parcours_profondeur(G, sommet, liste)
    return liste


print(parcours_profondeur(G, "A", []))
print(parcours_profondeur(G, "G", []))
