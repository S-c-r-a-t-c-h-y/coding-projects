from turtle import *
from random import *
import math
import time


class Polygone:
    """Classe qui modélise un polygone"""
    
    # Constructeur de la classe Polygone
    def __init__(self, nb_cote, cote, abscisse, ordonnee, fill):
        self.__cote = cote
        self.__abscisse = abscisse
        self.__ordonnee = ordonnee
        self.__nb_cote = nb_cote
        self.fill = fill # valeur boolénne qui décide ou non de remplir le pentagone
        
    def get_cote(self):
        return self.__cote
    
    def get_nb_cote(self):
        return self.__nb_cote
    
    def get_abscisse(self):
        return self.__abscisse
    
    def get_ordonnee(self):
        return self.__ordonnee
        
    # Méthode pour afficher le polygone au sommet supérieur (abscisse ; ordonnee)
    def afficher(self):
        # se référer au polygone de sierpinski pour des explications
        head = heading()
        setheading(0)
        
        if self.fill:
            begin_fill()
            
        goto(self.get_abscisse(), self.get_ordonnee())
        down()
        
        nb_cote = self.get_nb_cote()
        
        right(360 / (nb_cote * 2))
        for _ in range(nb_cote):
            forward(self.get_cote())
            right(360 / nb_cote)
            
        if self.fill:
            end_fill()
        up()
        
        setheading(head)
  

def sierpinski(n, longueur, a, o):
    head = heading()
    setheading(0)
    
    nouvelle_longueur = longueur * RATIO_COTE
     
    if n >= 1:
        left(360 / (nb_cote * 2))
        for _ in range(nb_cote):
            right(360 / nb_cote)
            up()
            
            avancement = longueur - nouvelle_longueur
            
            if nb_cote >= 9:
                # valeurs obtenus à tatons et rentrées dans une feuille excel
                # servant à corriger une erreur se produisant avec 9 ou plus côtés
                pente = 0.093714285714286
                origine = 1.02866666666667
                avancement *= (pente * (nb_cote-8) + origine)

            forward(avancement)
            
            down()
            sierpinski(n-1, nouvelle_longueur, position()[0], position()[1])
     
    else:
        # cas terminal
        
        # les polygones ne sont pas remplis, changer le False pour
        # True pour les remplir
        Polygone(nb_cote, longueur, a, o, False).afficher()
    
    setheading(head)

speed(0) # vitesse la plus rapide
colormode(255)

n = 2
longueur = 100
a = 0
o = 200
nb_cote = 6

def polygone_sierpinski(n, nb_cote, longueur, a, o):
    up()
    goto(a, o)

    global RATIO_PARTIE, RATIO_COTE
    
    RATIO_PARTIE = 2 * math.cos(math.radians(360 / nb_cote)) # relation de taille entre les niveaux de profondeur de pentagones
    RATIO_COTE = 1 / (RATIO_PARTIE + 2) # relation entre la taille du pentagon et la longueur du côté
    
    sierpinski(n, longueur, a, o)

    ht() # pour cacher la tortue

polygone_sierpinski(n, nb_cote, longueur, a, o)

# https://mathcurve.com/fractals/sierpinski/sierpinski.shtml