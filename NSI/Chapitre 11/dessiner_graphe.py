import matplotlib.pyplot as plt
import networkx as nwx
import pylab


G1 = nwx.Graph()


def dessiner1(G):
    """Fonction qui permet de dessiner un graphe simple non orienté
    défini à partir d'un dictionnaire
    """
    liste_sommets = [cle for cle in G]
    liste_aretes = []
    for cle in G:
        for s1 in G[cle]:
            liste_aretes.append((cle, s1))
    G1.add_nodes_from(liste_sommets)
    G1.add_edges_from(liste_aretes)
    nwx.draw(G1, with_labels=True, font_weight="bold", node_size=800, node_color="red")  # on peut aussi essayer avec :
    plt.show()


def dessiner2(G):
    """Fonction qui permet de dessiner un graphe simple non orienté
    défini à partir d'une matrice d'adjacence
    """
    liste_sommets = [i for i in range(len(G))]
    liste_aretes = []
    for i in range(len(G)):
        for j in range(i + 1):
            if G[i][j] == 1:
                liste_aretes.append((i, j))
    G1.add_nodes_from(liste_sommets)
    G1.add_edges_from(liste_aretes)
    nwx.draw(G1, with_labels=True, font_weight="bold", node_size=800, node_color="red")  # on peut aussi essayer avec :
    plt.show()


def dessiner3(G):
    """Fonction qui permet de dessiner un graphe simple non orienté pondéré
    défini à partir d'une matrice des poids
    """
    liste_sommets = [i for i in range(len(G))]
    liste_aretes = []
    for i in range(len(G)):
        for j in range(i):
            if G[i][j] > 0:
                liste_aretes.append((i, j, G[i][j]))

    G1.add_nodes_from(liste_sommets)
    G1.add_weighted_edges_from(liste_aretes)
    edge_labels = {(u, v): p for (u, v, p) in liste_aretes}
    pos = nwx.spring_layout(G1)
    nwx.draw_networkx_edge_labels(G1, pos, edge_labels=edge_labels)
    nwx.draw(G1, pos, with_labels=True, font_weight="bold", node_size=800, node_color="red")  # on peut aussi essayer avec :
    pylab.show()
