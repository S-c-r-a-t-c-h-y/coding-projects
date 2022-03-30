from dessiner_graphe import *

G = {
    "A": ["E", "B"],
    "B": ["A", "E", "C"],
    "C": ["B", "D"],
    "D": ["C", "B", "E"],
    "E": ["D", "B", "A", "F"],
    "F": ["G", "H", "E"],
    "G": ["F"],
    "H": ["F"],
}

dessiner1(G)
