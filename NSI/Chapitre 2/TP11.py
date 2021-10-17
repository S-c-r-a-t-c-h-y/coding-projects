from turtle import *
from random import *
  
  
def branche(n, longueur):
    """ Fonction récursive qui trace les branches de l'arbre """
    if n >= 1: # la condition d'arrêt est n == 0
        width(2*n-1) # largeur des branches
        forward(longueur) # on trace une branche
        branche(n-1, 0.7 * longueur)
        right(angle) 
        branche(n-1, 0.7 * longueur) # premier appel récursif
        left( 2 * angle ) 
        branche(n-1, 0.7 * longueur) # deuxième appel récursif        
        up()
        right(angle) 
        backward(longueur)
        down()


speed('fastest') # vitesse la plus rapide
right(-90)  
angle = 20
color('brown')
up()
goto(0,-300)
down()
branche(6, 150)