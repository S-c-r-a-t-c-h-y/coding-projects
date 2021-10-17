from turtle import *

LONGUEUR = 100
LARGEUR = 20

class Rectangle:
    """Classe modélisant un rectangle"""
    
    compteur = 0 
    
    # Constructeur
    def __init__(self, l, h, a, o, c):
        """Initialise les valeurs des attributs"""
        self.largeur = l
        self.hauteur = h
        self.abscisse = a
        self.ordonnee = o
        self.couleur = c
        Rectangle.compteur += 1
        
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
        
        
class Carre(Rectangle):
    
    def __init__(self, cote, a, o, c):
        super().__init__(cote, cote, a, o ,c)
        
        
rectangle1 = Rectangle(LONGUEUR, LARGEUR, 0, 0, 'blue')
rectangle2 = Rectangle(LARGEUR, LONGUEUR, LONGUEUR, 0, 'red')
rectangle3 = Rectangle(LONGUEUR, LARGEUR, LARGEUR, LONGUEUR, 'green')
rectangle4 = Rectangle(LARGEUR, LONGUEUR, 0, LARGEUR, 'yellow')
carre1 = Carre(LONGUEUR-LARGEUR, LARGEUR, LARGEUR, 'orange')

print(f"Le nombre d'instance de la classe Rectangle est {Rectangle.compteur} .")

rectangle1.afficher()
rectangle2.afficher()
rectangle3.afficher()
rectangle4.afficher()

carre1.afficher()

