from pile import *
from file import *
from dessiner_graphe import *


M = [
    [0, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 1, 0, 1, 0],
    [1, 1, 1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0],
]

dessiner2(M)


def parcours_profondeur3(G, s, liste):
    """Fonction récursive qui retourne sous forme de liste un parcours
    en profondeur du graphe G dont les sommets sont numérotés de 0  à  len(G)
    """
    liste.append(s)
    for a in range(len(G[s])):
        if G[s][a] == 1:
            if a not in liste:
                parcours_profondeur3(G, a, liste)
    return liste


def adjacents(G, s):
    return [i for i in range(len(G[s])) if G[s][i] == 1]


def parcours_profondeur4(G, s):
    l = []
    p = Pile()
    p.empiler(s)
    while not p.est_vide():
        s = p.depiler()
        if s not in l:
            l.append(s)
        for a in adjacents(G, s):
            if a not in l:
                p.empiler(a)
    return l


def parcours_largeur(G, s):
    l = []
    f = File()
    f.enfiler(s)
    while not f.est_vide():
        s = f.defiler()
        if s not in l:
            l.append(s)
            for a in adjacents(G, s):
                if a not in l:
                    f.enfiler(a)
    return l


# print(parcours_profondeur3(M, 0, []))
# print(parcours_profondeur3(M, 6, []))

# print(adjacents(M, 0))
# print(adjacents(M, 6))
# print(adjacents(M, 5))

# print(parcours_profondeur4(M, 0))
# print(parcours_profondeur4(M, 6))

print(parcours_largeur(M, 0))
print(parcours_largeur(M, 6))
