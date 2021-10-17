from turtle import *
from random import *
  
  
def branche(n, longueur):
    """ Fonction récursive qui trace les branches de l'arbre """
    if n >= 2: # la condition d'arrêt est n == 0
        color('brown')
        angle1, angle2, angle3 = randint(-20, 20), randint(20, 40), randint(20, 40)
        width(2*n-1) # largeur des branches
        forward(longueur) # on trace une branche
        
        right(angle1)
        branche(n-1, 0.7 * longueur)
        right(angle2)
        branche(n-1, 0.7 * longueur) # premier appel récursif
        left(angle1 + angle2 + angle3) 
        branche(n-1, 0.7 * longueur) # deuxième appel récursif        
        up()
        right(angle3) 
        backward(longueur)
        down()
    else:
        color('green')
        width(20)
        forward(longueur*2)
        backward(longueur*2)


speed('fastest') # vitesse la plus rapide
right(-90)  
color('brown')
up()
goto(0,-300)
down()
branche(6, 150)

