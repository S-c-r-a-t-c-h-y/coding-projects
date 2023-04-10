from turtle import *
from random import *


class Triangle:
    """Classe qui modélise un triangle"""
    
    # Constructeur de la classe Triangle
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
        
    # Méthode pour afficher le triangle au coin supérieur gauche (abscisse ; ordonnee)
    def afficher(self):
        begin_fill()
        goto(self.get_abscisse(), self.get_ordonnee())
        down()
        forward(self.get_cote())
        right(120)
        forward(self.get_cote())
        right(120)
        forward(self.get_cote())
        right(120)
        end_fill()
        up()
  
def triangle(n, longueur, a, o):
    """ Fonction récursive qui trace le tapis de sierpinski """
    
    def recursion(n, longueur, a, o):
        """ fonction récursive qui s'occupent de dessiner les triangles blancs"""
        c = longueur // 2
        
        if n != 0:
            p = 1.5 * c
            hauteur = (2/c) * (p*(p-c)**3) ** 0.5
            
            color('white')
            Triangle(c, a+c/2, o+hauteur).afficher()
            
            recursion(n-1, c, a, o)
            recursion(n-1, c, a+c/2, o+hauteur)
            recursion(n-1, c, a+c, o)
    
    # déssine le triangle de base
    # (je trace des carrés blancs à l'intérieur d'un triangle noir inversé
    # au lieu de tracer des carrés noirs directements)
    color('black')
    begin_fill()
    goto(a, o)
    down()
    forward(longueur)
    left(120)
    forward(longueur)
    left(120)
    forward(longueur)
    left(120)
    end_fill()
    up()
    
    recursion(n, longueur, a, o)
   

speed('fastest') # vitesse la plus rapide
up() # relève le stylo
colormode(255)

n = 6
longueur = 600
a = -300
o = -250

triangle(n, longueur, a, o)

ht() # pour cacher la tortue