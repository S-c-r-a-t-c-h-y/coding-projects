from turtle import setworldcoordinates, Turtle, tracer, setup, exitonclick
from dessiner_graphe import dessiner_graphe_labyrinthe
from file import *
from mazelib import maze

from random import randint, choice
from time import sleep


class labyrinthe:
    def __init__(self, nb_lignes, nb_colonnes, depart=None, arrivee=None):
        self.u = 10  # taille d'un mur
        self.nb_lignes = nb_lignes
        self.nb_colonnes = nb_colonnes

        self.depart = (0, 0) if depart is None else depart
        self.arrivee = (nb_lignes - 1, nb_colonnes - 1) if arrivee is None else arrivee

        self.generer_labyrinthe(nb_colonnes, nb_lignes)
        self.graphe = None

    def regenerer(self):
        m = maze(self.nb_lignes, self.nb_colonnes)
        m.CreateMaze()
        self.murs = []
        for i in range(self.nb_lignes):
            liste = []
            for j in range(self.nb_colonnes):
                liste.append(0)
            self.murs.append(liste)
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                self.murs[i][j] = [m.maze_map[(i + 1, j + 1)]["N"], m.maze_map[(i + 1, j + 1)]["E"], m.maze_map[(i + 1, j + 1)]["S"], m.maze_map[(i + 1, j + 1)]["W"]]

        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                for k in range(4):
                    self.murs[i][j][k] = not (self.murs[i][j][k])

    def dessiner(self):
        setup(500, 500, 100, 100)
        setworldcoordinates(-1, -(self.nb_lignes * self.u + 1), self.nb_colonnes * self.u + 1, 1)
        t = Turtle()
        t.hideturtle()  # cache la tortue
        tracer(20)  # supprime l'animation

        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                t.penup()
                t.goto(j * self.u, -i * self.u)
                t.setheading(0)
                for k in range(4):
                    if self.murs[i][j][k]:
                        t.pendown()
                    else:
                        t.penup()
                    t.forward(self.u)
                    t.right(90)
        exitonclick()

    def dessiner_chemin(self, chemin=None):
        if chemin is None:
            chemin = self.determiner_chemin()

        setup(500, 500, 100, 100)
        setworldcoordinates(-1, -(self.nb_lignes * self.u + 1), self.nb_colonnes * self.u + 1, 1)
        t = Turtle()
        t.hideturtle()  # cache la tortue
        tracer(20)  # supprime l'animation

        # dessine les murs
        x_vals = {}
        for i in range(self.nb_lignes):
            y = -i * self.u
            for j in range(self.nb_colonnes):
                if j not in x_vals:
                    x_vals[j] = j * self.u
                t.penup()
                t.goto(x_vals[j], y)
                t.setheading(0)
                for k in range(4):
                    if self.murs[i][j][k]:
                        t.pendown()
                    else:
                        t.penup()
                    t.forward(self.u)
                    t.right(90)

        # dessine la case de depart en vert
        t.penup()
        t.fillcolor("green")
        t.goto(self.depart[1] * self.u + 1, -self.depart[0] * self.u - 1)
        t.begin_fill()
        for _ in range(4):
            t.forward(self.u - 2)
            t.right(90)
        t.end_fill()

        # dessine la case d'arrivée en rouge
        t.fillcolor("red")
        t.goto(self.arrivee[1] * self.u + 1, -self.arrivee[0] * self.u - 1)
        t.begin_fill()
        for _ in range(4):
            t.forward(self.u - 2)
            t.right(90)
        t.end_fill()

        # dessine le chemin
        t.penup()
        t.color("red")
        pensize = 1000 // max(self.nb_lignes * self.u, self.nb_colonnes * self.u)
        t.pensize(pensize)
        t.goto(chemin[0][1] * self.u + self.u // 2, -chemin[0][0] * self.u - self.u // 2)
        t.pendown()
        for i, j in chemin[1:]:
            t.goto(j * self.u + self.u // 2, -i * self.u - self.u // 2)

        t.penup()
        exitonclick()

    def creer_graphe(self):
        self.graphe = {}
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                self.graphe[(i, j)] = []
                if not self.murs[i][j][0] and i != 0:
                    self.graphe[(i, j)].append((i - 1, j))
                if not self.murs[i][j][1] and j != self.nb_colonnes - 1:
                    self.graphe[(i, j)].append((i, j + 1))
                if not self.murs[i][j][2] and i != self.nb_lignes - 1:
                    self.graphe[(i, j)].append((i + 1, j))
                if not self.murs[i][j][3] and j != 0:
                    self.graphe[(i, j)].append((i, j - 1))
        return self.graphe

    def determiner_chemin(self):
        if self.graphe is None:
            self.creer_graphe()
        pere = {}
        f = File()
        f.enfiler(self.depart)
        l = []
        while not f.est_vide():
            s = f.defiler()
            if s == self.arrivee:
                break
            if s not in l:
                l.append(s)
                for a in self.graphe[s]:
                    if a not in l:
                        f.enfiler(a)
                        pere[a] = s

        precedent = pere[self.arrivee]
        parcours = [self.arrivee]
        while precedent != self.depart:
            parcours.append(precedent)
            precedent = pere[precedent]
        parcours.append(self.depart)
        parcours = list(reversed(parcours))
        return parcours

    def generer_labyrinthe(self, width, height):
        """Genere un labyrinthe aleatoirement en utilisant l'algorithme de prim
        https://weblog.jamisbuck.org/2011/1/10/maze-generation-prim-s-algorithm
        """
        N, E, S, W = 0, 1, 2, 3
        OPPOSITE = {N: S, S: N, W: E, E: W}

        IN = 0x10
        FRONTIER = 0x20

        self.murs = [[[True, True, True, True] for _ in range(width)] for _ in range(height)]
        grid = [[0 for _ in range(width)] for _ in range(height)]
        frontier = []

        def add_frontier(x, y, grid, frontier):
            if x >= 0 and y >= 0 and y < height and x < width and grid[y][x] == 0:
                grid[y][x] = grid[y][x] | FRONTIER
                frontier.append([x, y])

        def mark(x, y, grid, frontier):
            grid[y][x] = grid[y][x] | IN
            add_frontier(x - 1, y, grid, frontier)
            add_frontier(x, y - 1, grid, frontier)
            add_frontier(x, y + 1, grid, frontier)
            add_frontier(x + 1, y, grid, frontier)

        def neighbors(x, y, grid):
            n = []
            if x > 0 and grid[y][x - 1] & IN != 0:
                n.append([x - 1, y])
            if x + 1 < width and grid[y][x + 1] & IN != 0:
                n.append([x + 1, y])
            if y > 0 and grid[y - 1][x] & IN != 0:
                n.append([x, y - 1])
            if y + 1 < height and grid[y + 1][x] & IN != 0:
                n.append([x, y + 1])
            return n

        def direction(fx, fy, tx, ty):
            return E if fx < tx else W if fx > tx else S if fy < ty else N

        mark(randint(0, width - 1), randint(0, height - 1), grid, frontier)
        while frontier:
            x, y = frontier.pop(randint(0, len(frontier) - 1))
            n = neighbors(x, y, grid)
            nx, ny = choice(n)

            dir = direction(x, y, nx, ny)

            self.murs[y][x][dir] = False
            self.murs[ny][nx][OPPOSITE[dir]] = False

            mark(x, y, grid, frontier)

        return self.murs


if __name__ == "__main__":
    width, height = 25, 25
    lab1 = labyrinthe(height, width)
    lab1.dessiner_chemin()
