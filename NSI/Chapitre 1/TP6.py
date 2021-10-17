from turtle import *

class Rectangle:
    """Classe modélisant un rectangle"""
    
    # Constructeur
    def __init__(self, l, h, a, o, c):
        """Initialise les valeurs des attributs"""
        self.largeur = l
        self.hauteur = h
        self.abscisse = a
        self.ordonnee = o
        self.couleur = c
        
    # Méthode afficher()
    def afficher(self):
        color(self.couleur)
        begin_fill()
        goto(self.abscisse, self.ordonnee)
        down()
        forward(self.largeur)
        left(90)
        forward(self.hauteur)
        left(90)
        forward(self.largeur)
        left(90)
        forward(self.hauteur)
        left(90)
        end_fill()
        up()
        
rectangle1 = Rectangle(100, 50, 0, 0, 'blue')
rectangle1.afficher()