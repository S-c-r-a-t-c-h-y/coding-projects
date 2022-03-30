from dessiner_graphe import *


def matrice(G):
    """Fonction qui prend un graphe G au format dictionnaire en paramètre
    et qui retourne un graphe G2 au format matrice
    """
    G2 = []
    sommets = list(G.keys())
    for adjacents in G.values():
        l = [0] * len(sommets)
        for a in adjacents:
            l[sommets.index(a)] = 1
        G2.append(l)
    return G2


def dico(G):
    """Fonction qui prend un graphe G au format matrice en paramètre
    et qui retourne un graphe G1 au format dictionnaire
    """
    G1 = {i: [] for i in range(len(G))}

    for i, ligne in enumerate(G):
        for j, elem in enumerate(ligne):
            if elem == 1:
                G1[i].append(j)

    return G1


G = {
    "A": ["B", "C", "D"],
    "B": ["A", "E", "F"],
    "C": ["A", "G"],
    "D": ["A"],
    "E": ["B"],
    "F": ["B"],
    "G": ["C"],
}

M = [
    [0, 1, 1, 1, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 1, 0, 1, 0],
    [1, 1, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 1],
    [0, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 1, 1, 0],
]

# G2 = matrice(G)
# dessiner2(G2)

G1 = dico(M)
dessiner1(G1)
