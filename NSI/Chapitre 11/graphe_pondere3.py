from dessiner_graphe import *

G = [
    [0, 1, 4, 0, 0, 8, 0],
    [1, 0, 3, 1, 3, 0, 0],
    [4, 3, 0, 5, 0, 1, 0],
    [0, 1, 5, 0, 8, 0, 0],
    [0, 3, 0, 8, 0, 2, 7],
    [8, 0, 1, 0, 2, 0, 4],
    [0, 0, 0, 0, 7, 4, 0],
]


def dijkstra(G, i, j):
    poids = {k: (float("inf"), None) for k in range(len(G))}
    poids[i] = (0, None)
    poids_non_visite = poids.copy()
    selectionne = i
    while True:
        del poids_non_visite[selectionne]
        for k in range(len(G)):
            a = G[selectionne][k]
            if a != 0 and poids[k][0] > a + poids[selectionne][0]:
                poids[k] = (poids[selectionne][0] + a, selectionne)
                poids_non_visite[k] = poids[k]
        if selectionne == j:
            break
        selectionne = min({a: e[0] for a, e in poids_non_visite.items()}, key=poids.get)
    print(poids)
    precedent = poids[j][1]
    chemin = [j]
    while precedent is not None:
        chemin.append(precedent)
        precedent = poids[precedent][1]
    chemin = list(reversed(chemin))
    return (chemin, poids[j][0])


print(dijkstra(G, 0, 4))
print(dijkstra(G, 6, 1))
dessiner3(G)
