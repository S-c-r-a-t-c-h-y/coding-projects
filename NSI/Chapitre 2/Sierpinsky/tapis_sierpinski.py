
from turtle import *
from random import *


class Carre:
    """Classe qui modélise un carré"""
    
    # Constructeur de la classe Carre
    def __init__(self, cote, abscisse, ordonnee):
        self.__cote = cote
        self.__abscisse = abscisse
        self.__ordonnee = ordonnee
        
    def get_cote(self):
        return self.__cote
    
    def get_abscisse(self):
        return self.__abscisse
    
    def get_ordonnee(self):
        return self.__ordonnee
        
    # Méthode pour afficher le carré au coin inférieur gauche (abscisse ; ordonnee)
    def afficher(self):
        begin_fill()
        goto(self.get_abscisse(), self.get_ordonnee())
        down()
        forward(self.get_cote())
        left(90)
        forward(self.get_cote())
        left(90)
        forward(self.get_cote())
        left(90)
        forward(self.get_cote())
        left(90)
        end_fill()
        up()
  
  
def tapis(n, longueur, a, o):
    """ Fonction récursive qui trace le tapis de sierpinski """  
    
    def carre(n, longueur, a, o):
        """ fonction récursive qui permet de tracer le tapis de Sierpinski"""
        
        color(liste_couleur[n])
        c = longueur // 3
        
        if n != 0:
            Carre(c, a+c, o+c).afficher()
            for i in range(3):
                for j in range(3):
                    if (i, j) != (1, 1): # carre du milieu
                        carre(n-1, c, a+c*i, o+c*j)
    
    Carre(longueur, a, o).afficher()
    carre(n, longueur, a, o)
    
                    
nb_couleur = 5
liste_couleur = [(randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(nb_couleur)]

speed('fastest') # vitesse la plus rapide
up() # relève le stylo
colormode(255)
color(liste_couleur[-1])

n = 3
longueur = 300
a = 0
o = 0

tapis(n, longueur, a, o)

ht() # pour cacher la tortue