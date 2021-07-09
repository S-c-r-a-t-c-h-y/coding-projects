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
        pomme_coords = [randrange(0, 495, taille_carre), randrange(0, 495, taille_carre)]

def update():
    """
    Focntion qui s'éxecute toutes les 60 ms qui prend en charge l'affichage du serpent,
    la mise à jour des positions de son corps et la détection des collisions avec son
    corps et avec les murs.
    """

    global fenetre, canvas, snake, direction, derniere_direction, pomme_coords, score, text_score
    canvas.delete('all')

    # on dessine la pomme, la tête du serpent puis son corps
    canvas.create_rectangle(pomme_coords[0], pomme_coords[1],
        pomme_coords[0] + taille_carre, pomme_coords[1] + taille_carre,
        outline='white', fill='red')

    canvas.create_rectangle(snake[-1][0], snake[-1][1], snake[-1][0] + taille_carre, snake[-1][1] + taille_carre, outline='white', fill='blue')
    for part in snake[:-1]:
        canvas.create_rectangle(part[0], part[1], part[0] + taille_carre, part[1] + taille_carre, outline='white', fill='black')


    # on effectue le changement de position selon la direction du serpent
    if snake[-1][0] != pomme_coords[0] or snake[-1][1] != pomme_coords[1]: # si le serpent ne se trouve pas sur une pomme
        snake.pop(0)
    else:
        placer_pomme()
        score += 1
        text_score.set('Score : ' + str(score))
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
    if snake[-1][0] < 0 or snake[-1][0] >= 600 or snake[-1][1] < 0 or snake[-1][1] >= 495:
        tkinter.messagebox.showinfo(title='Perdu !', message=f'Vous êtes rentré dans un mur !')
        recommencer()

    derniere_direction = direction
    fenetre.after(100, update)
    

def recommencer():
    """
    Remet chaque paramètre à sa valeur initiale (snake, pomme, direction) afin de recommencer instantanément
    """

    global canvas, snake, direction, taille_carre, score
    canvas.delete('all')
    placer_pomme()
    snake = [[300 + 3 * taille_carre, 300], [300 + 2 * taille_carre, 300], [300 + taille_carre, 300], [300, 300]]
    direction = 'left'
    score = 0
    text_score.set('Score : ' + str(score))


# ------------------------------------------------------------------------------------------------------------------

def main():
    
    # initialisation de la fenêtre
    global fenetre
    fenetre = Tk()
    fenetre.title("Jeu du snake")
    fenetre.geometry('600x600')
    fenetre.configure(bg='white')
    fenetre.resizable(width=False, height=False)

    global taille_carre
    taille_carre = 20

    # canvas sur lequel le serpent et la pomme sont dessinés
    global canvas, snake, direction, derniere_direction, score, text_score
    canvas = Canvas(fenetre, width=600, height=495, bg='gray25')
    canvas.pack()

    # initialisation du serpent : c'est une liste de liste contenant les coordonnées de son corps
    # l'élément d'index -1 contient sa tête et l'élément d'index 0 sa queue
    snake = [[300 + 3 * taille_carre, 300], [300 + 2 * taille_carre, 300], [300 + taille_carre, 300], [300, 300]]
    direction = 'left'
    derniere_direction = direction

    # création des boutons 'recommencer', 'commencer' et 'quitter'
    bouton_recommencer = Button(fenetre, text='recommencer', command=recommencer, width=26, height=6, bg='grey')
    bouton_recommencer.pack(side=LEFT)

    bouton_quitter = Button(fenetre, text='quitter', command=fenetre.destroy, width=26, height=6, bg='grey')
    bouton_quitter.pack(side=LEFT)

    score = 0
    text_score = StringVar()
    text_score.set("Score : " + str(score))
    label_score = Label(fenetre, textvariable=text_score, font='Times 20 bold', bg='white', fg='black', height=1, width=12)
    label_score.pack(side=LEFT)

    placer_pomme()
    update()

    # linkage des touches 'zqsd' du clavier avec les fonctions qui permettent de changer la direction du serpent
    fenetre.bind("<z>", up)
    fenetre.bind("<s>", down)
    fenetre.bind("<q>", left)
    fenetre.bind("<d>", right)
    fenetre.mainloop()

if __name__ == '__main__':
    main()