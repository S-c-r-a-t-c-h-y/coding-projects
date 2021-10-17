from turtle import *


def courbe_koch(n, longueur):
    """Fonction récursive qui trace la courbe de Koche pour un rang n fixé"""
    if n == 0 :
        forward(longueur)
    else :
        courbe_koch(n-1, longueur/3)
        left(60)
        courbe_koch(n-1, longueur/3)
        right(120)
        courbe_koch(n-1, longueur/3)
        left(60)
        courbe_koch(n-1, longueur/3)

n1 = 1  # rang de la courbe de Koch
longueur1 = 300  # longueur au rang 0
up()  # on lève la pointe du stylo
goto(-300, 0)  # on déplace la tortue pour centrer la courbe
down()  # on abaisse la pointe du stylo
setheading(0) # orientation intiale de la tête : vers la droite de l'écran
hideturtle() # on cache la tortue
speed(0)  # on accélère la tortue
color('green')  # couleur de la courbe
courbe_koch(3, longueur1) 