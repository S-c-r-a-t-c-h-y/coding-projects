from turtle import *
from random import *
import math


class Pentagone:
    """Classe qui modélise un pentagone"""
    
    # Constructeur de la classe Pentagone
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
        
    # Méthode pour afficher le pentagone au sommet supérieur (abscisse ; ordonnee)
    def afficher(self):
        
        # on stock l'orientation de la tortue avant de dessiner le pentagone
        head = heading()
        setheading(0) # réinitialise l'orientation de la tortue
        
        begin_fill()
        goto(self.get_abscisse(), self.get_ordonnee())
        down()
        right(36)
        for i in range(5):
            forward(self.get_cote())
            right(72)
        end_fill()
        up()
        
        setheading(head) # on retrouve l'orientation initiale
  

def sierpinski(n, longueur, a, o):
    """ fonction récursive qui permet de dessiner le pentagone de sierpinski"""
    head = heading()
    setheading(0)
    
    nouvelle_longueur = longueur * RATIO_COTE
    
    if n >= 1:
        left(36)
        for j in range(5):
            right(72)
            up()
            forward(longueur * RATIO_COTE / RATIO_PARTIE)
            down()
            sierpinski(n-1, nouvelle_longueur, position()[0], position()[1])
     
    else:
        # cas terminal
        Pentagone(longueur, a, o).afficher()
    
    setheading(head)

speed(0) # vitesse la plus rapide
colormode(255)

# ces valeurs ont été trouvées sur internet, ce sont des rapports d'homothétie
RATIO_PARTIE = 2 * math.cos(math.radians(72)) # relation de taille entre les niveaux de profondeur de pentagoneeees
RATIO_COTE = 1 / (RATIO_PARTIE + 2) # relation entre la taille du pentagoneee et la longueur du côté

n = 2
longueur = 300
a = 0
o = 0

longueur *= RATIO_PARTIE
sierpinski(n, longueur, a, o)

ht() # pour cacher la tortue
