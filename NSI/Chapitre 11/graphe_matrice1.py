from pile import *
from file import *
from dessiner_graphe import *


M = [
    [0, 1, 1, 1, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0],
    [1, 0, 0, 1, 0, 1, 0],
    [1, 1, 1, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 1, 1],
    [0, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 1, 1, 0],
]

dessiner2(M)


def parcours_profondeur3(G, s, liste):
    """Fonction récursive qui retourne sous forme de liste un parcours
    en profondeur du graphe G dont les sommets sont numérotés de 0  à  len(G)
    """
    liste.append(s)
    for a in range(len(G[s])):
        pass
