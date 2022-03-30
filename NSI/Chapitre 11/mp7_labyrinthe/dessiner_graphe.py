import matplotlib.pyplot as plt
import networkx as nx


def dessiner_graphe_labyrinthe(G, nb_lignes, nb_colonnes):
    """Fonction qui permet de dessiner un graphe simple non orienté
    défini à partir d'un dictionnaire
    """
    G1 = nx.Graph()

    pos = {}
    for i in range(nb_lignes):
        for j in range(nb_colonnes):
            pos[(i, j)] = (j, nb_lignes - i)

    liste_sommets = [cle for cle in G]
    liste_aretes = []
    for cle in G:
        for s1 in G[cle]:
            liste_aretes.append((cle, s1))
    G1.add_nodes_from(liste_sommets)
    G1.add_edges_from(liste_aretes)
    # nx.draw(G1, with_labels=True, font_weight="bold", node_size=800,node_color="red",pos=nwx.spring_layout(G1,seed=5))  # on peut aussi essayer avec :
    nx.draw(G1, with_labels=True, font_weight="bold", node_size=800, node_color="red", pos=pos)  # on peut aussi essayer avec :

    # plt.ion()
    plt.show()
