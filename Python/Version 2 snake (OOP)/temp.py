from tkinter import *
import tkinter.messagebox
from random import randrange

# ------------------------------------------------------------------------------------------------------------------
def up(event):
    """
    Fonction appelée quand la touche 'z' est pressée,
    elle définie la direction du serpent sur 'up' seulement si le serpent n'allait pas vers
    le bas (le serpent ne peut pas faire demi-tour)
    """
    global direction, derniere_direction
    if derniere_direction != 'down':
        direction = 'up'

def down(event):
    """
    Fonction appelée quand la touche 's' est pressée,
    elle définie la direction du serpent sur 'down' seulement si le serpent n'allait pas vers
    le haut (le serpent ne peut pas faire demi-tour)
    """
    global direction, derniere_direction
    if derniere_direction != 'up':
        direction = 'down'

def left(event):
    """
    Fonction appelée quand la touche 'q' est pressée,
    elle définie la direction du serpent sur 'left' seulement si le serpent n'allait pas vers
    la droite (le serpent ne peut pas faire demi-tour)
    """
    global direction, derniere_direction
    if derniere_direction != 'right':
        direction = 'left'

def right(event):
    """
    Fonction appelée quand la touche 'd' est pressée,
    elle définie la direction du serpent sur 'right' seulement si le serpent n'allait pas vers
    la gauche (le serpent ne peut pas faire demi-tour)
    """
    global direction, derniere_direction
    if derniere_direction != 'left':
        direction = 'right'
# ------------------------------------------------------------------------------------------------------------------

def placer_pomme():
    """
    Fonction qui défini les nouvelles coordonnées de la pomme en garantissant qu'elle ne se trouve pas dans la serpent
    """

    global pomme_coords, snake
    pomme_coords = snake[-1]
    while pomme_coords in snake:
        pomme_coords = [randrange(0, 495, 15), randrange(0, 495, 15)]

def update():
    """
    Focntion qui s'éxecute toutes les 60 ms qui prend en charge l'affichage du serpent,
    la mise à jour des positions de son corps et la détection des collisions avec son
    corps et avec les murs.
    """

    global fenetre, canvas, snake, direction, derniere_direction, pomme_coords
    canvas.delete('all')

    # on dessine la pomme, la tête du serpent puis son corps
    canvas.create_rectangle(pomme_coords[0], pomme_coords[1],
        pomme_coords[0] + taille_carre, pomme_coords[1] + taille_carre,
        outline='white', fill='red')

    canvas.create_rectangle(snake[-1][0], snake[-1][1], snake[-1][0] + taille_carre, snake[-1][1] + taille_carre, outline='white', fill='blue')
    for part in snake[:-1]:
        canvas.create_rectangle(part[0], part[1], part[0] + taille_carre, part[1] + taille_carre, outline='white', fill='black')


    # on effectue le changement de position selon la direction du serpent
    if snake[-1][0] != pomme_coords[0] or snake[-1][1] != pomme_coords[1]:
        snake.pop(0)
    else:
        placer_pomme()
    if direction == 'up':
        snake.append([snake[-1][0], snake[-1][1] - taille_carre])
    elif direction == 'down':
        snake.append([snake[-1][0], snake[-1][1] + taille_carre])
    elif direction == 'left':
        snake.append([snake[-1][0] - taille_carre, snake[-1][1]])
    elif direction == 'right':
        snake.append([snake[-1][0] + taille_carre, snake[-1][1]])

    # si la tête du serpent rentre dans son corps, c'est perdu
    if snake[-1] in snake[:-1]:
        tkinter.messagebox.showinfo(title='Perdu !', message=f'Vous vous êtes rentré dedans !')
        recommencer()

    # si la tête du serpent rentre dans un mur, c'est perdu aussi
    if snake[-1][0] < 0 or snake[-1][0] > 600 or snake[-1][1] < 0 or snake[-1][1] > 495:
        tkinter.messagebox.showinfo(title='Perdu !', message=f'Vous êtes rentré dans un mur !')
        recommencer()

    derniere_direction = direction
    fenetre.after(60, update)
    

def recommencer():
    """
    Détruit le canvas et en recréé un autre en rappelant la fonction main()
    """
    fenetre.destroy()
    main()

def commencer():
    """
    Place la pomme et commence le déplacement du serpent ainsi que son affichage
    """
    placer_pomme()
    update()

# ------------------------------------------------------------------------------------------------------------------

