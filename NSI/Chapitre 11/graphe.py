import matplotlib.pyplot as plt
import networkx as nwx
from collections import deque


class Graphe:
    """Classe qui modélise un graphe orienté."""

    def __init__(self):
        self._dict = {}

    def ajouter_sommet(self, sommet, liaisons=None):
        if liaisons is None:
            liaisons = []

        self._dict[sommet] = liaisons

    def ajouter_liasons(self, sommet, liaisons):
        if isinstance(liaisons, (list, tuple)):
            self._dict[sommet].extend(liaisons)
        else:
            self._dict[sommet].append(liaisons)

    def distance(self, depart, arrive, chemin=None):
        if depart == arrive:
            return 0
        if chemin is None:
            chemin = []
        chemin.append(depart)
        distances = [self.distance(a, arrive, chemin.copy()) + 1 for a in self.adjacents(depart) if a not in chemin]
        distances = [distance for distance in distances if distance != 0]
        return min(distances, default=-1)

    def sommets(self):
        return list(self._dict.keys())

    def ordre(self):
        return len(self._dict)

    def adjacents(self, sommet):
        return self._dict[sommet]

    def degre(self, sommet):
        return len(self.adjacents(sommet))

    def est_isole(self, sommet):
        return self.degre(sommet) == 0

    def excentricite(self, sommet):
        return max(self.distance(sommet, s) for s in self._dict)

    def rayon(self):
        return min(self.excentricite(s) for s in self._dict)

    def diametre(self):
        return max(self.excentricite(s) for s in self._dict)

    def centres(self):
        return [s for s in self._dict if self.excentricite(s) == self.rayon()]

    def est_connexe(self):
        pass

    def parcours_profondeur_recursif(self, sommet, liste=None):
        if liste is None:
            liste = []
        liste.append(sommet)
        for sommet in self.adjacents(sommet):
            if sommet not in liste:
                self.parcours_profondeur_recursif(sommet, liste)
        return liste

    def parcours_profondeur_iteratif(self, sommet):
        liste = []
        p = [sommet]  # pile
        while p:
            sommet = p.pop()
            if sommet not in liste:
                liste.append(sommet)
            for a in self.adjacents(sommet):
                if a not in liste:
                    p.append(a)
        return liste

    def dfs(self, sommet, liste=None):
        return self.parcours_profondeur_iteratif(sommet, liste)

    def parcours_largeur(self, sommet):
        liste = []
        f = deque()  # file
        f.append(sommet)
        while f:
            sommet = f.popleft()
            if sommet not in liste:
                liste.append(sommet)
            for a in self.adjacents(sommet):
                if a not in liste:
                    f.append(a)
        return liste

    def bfs(self, sommet):
        return self.parcours_largeur(sommet)

    def dessiner(self):
        G1 = nwx.DiGraph()
        liste_aretes = []
        for cle in self._dict:
            liste_aretes.extend((cle, s1) for s1 in self._dict[cle])
        G1.add_nodes_from(self.sommets())
        G1.add_edges_from(liste_aretes)
        nwx.draw(G1, with_labels=True, font_weight="bold", node_size=800, node_color="red")
        plt.show()

    def matrice(self):
        G2 = []
        for adjacents in self._dict.values():
            l = [0] * self.ordre()
            for a in adjacents:
                l[self.sommets().index(a)] = 1
            G2.append(l)
        return G2

    def from_matrice(self, matrice):
        """Fonction qui forme le graphe a partir de la matrice d'adjacence 'matrice'."""
        self._dict = {i: [] for i in range(len(matrice))}

        for i, ligne in enumerate(matrice):
            for j, elem in enumerate(ligne):
                if elem == 1:
                    self._dict[i].append(j)


if __name__ == "__main__":
    g = Graphe()
    g.ajouter_sommet("A")
    g.ajouter_sommet("B")
    g.ajouter_sommet("C", ["A", "B"])
    g.ajouter_sommet("D", ["A", "B"])

    g.ajouter_liasons("A", "C")
    g.ajouter_liasons("B", "C")

    g.dessiner()
