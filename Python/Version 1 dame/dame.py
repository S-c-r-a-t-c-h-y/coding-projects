from tkinter import *
import tkinter
import tkinter.messagebox

dx = 50 # distance entre le centre x d'une case et le centre x de la case d'à côté
dy = 50 # distance entre le centre y d'une case et le centre y de la case d'en dessous

tour = 0 # compteur de tour
pion_selectionne = None
table = [[0 for _ in range(10)] for _ in range(10)]

score_j1, score_j2 = 0, 0

# ------------------------------------------------------------------------------------------------------------------

def voisins(i: int, j: int) -> list:
    """
    Cette fonction retourne une liste contenant les coordonnées
    des cases voisines selon l'emplacement de la case et son contenu
    ainsi qu'une liste contenant l'emplacement d'une case où l'on se retrouverais si
    l'on prenais (prise) le pion à l'emplacement à l'index suivant
    
    :param i: de type int
    :param i: compris entre 0 et 9
    :param j: de type int
    :param j: compris entre 0 et 9
    :return: de type list
    """
    
    assert type(i) == int, "Le 1er paramètre doit être un entier."
    assert 0 <= i <= 9, "Le 1er paramètre doit être compris entre 0 et 9."
    assert type(j) == int, "Le 2eme paramètre doit être un entier."
    assert 0 <= j <= 9, "Le 2eme paramètre doit être compris entre 0 et 9."

    voisins_2 = [] # liste qui stock les cases sur lequelles le pion peut bouger en en prenant un autre

    if table[i][j] == 0: return [] # une case vide n'as pas de voisins

    if table[i][j] == 1: # pion du joueur 1
        voisins = [(i-1, j-1), (i-1, j+1)]
        try:
            if (table[i-1][j-1] == 2 or table[i-1][j-1] == 4) and table[i-2][j-2] == 0:
                voisins_2.append((i-2, j-2))
                voisins_2.append((i-1, j-1))
        except:
            pass

        try:
            if (table[i-1][j+1] == 2 or table[i-1][j+1] == 4) and table[i-2][j+2] == 0:
                voisins_2.append((i-2, j+2))
                voisins_2.append((i-1, j+1))
        except:
            pass

    elif table[i][j] == 2: # pion du joueur 2
        voisins = [(i+1, j-1), (i+1, j+1)]

        try:
            if (table[i+1][j-1] == 1 or table[i+1][j-1] == 3) and table[i+2][j-2] == 0:
                voisins_2.append((i+2, j-2))
                voisins_2.append((i+1, j-1))
        except:
            pass

        try:
            if (table[i+1][j+1] == 1 or table[i+1][j+1] == 3) and table[i+2][j+2] == 0:
                voisins_2.append((i+2, j+2))
                voisins_2.append((i+1, j+1))
        except:
            pass

    else: # dame quelconque
        voisins = []
        # on regarde toute les case dans toutes les diagonales jusqu'à ce qu'on atteigne une case occupé ou un bord
        for k in range(1,11):
            try:
                if table[i-k][j+k] != 0:
                    break
                voisins.append((i-k, j+k))
            except:
                k -= 1
                break
        try:
            case = table[i-k][j+k]
            if (((case == 2 or case == 4) and table[i][j] == 3) or ((case == 1 or case == 3) and table[i][j] == 4)) and table[i-k-1][j+k+1] == 0:
                voisins_2.append((i-k-1, j+k+1))
                voisins_2.append((i-k, j+k))
        except:
            pass

        for k in range(1,11):
            try:
                if table[i-k][j-k] != 0:
                    break
                voisins.append((i-k, j-k))
            except:
                break
        try:
            case = table[i-k][j-k]
            if (((case == 2 or case == 4) and table[i][j] == 3) or ((case == 1 or case == 3) and table[i][j] == 4)) and table[i-k-1][j-k-1] == 0:
                voisins_2.append((i-k-1, j-k-1))
                voisins_2.append((i-k, j-k))
        except:
            pass

        for k in range(1,11):
            try:
                if table[i+k][j+k] != 0:
                    break
                voisins.append((i+k, j+k))
            except:
                break
        try:
            case = table[i+k][j+k]
            if (((case == 2 or case == 4) and table[i][j] == 3) or ((case == 1 or case == 3) and table[i][j] == 4)) and table[i+k+1][j+k+1] == 0:
                voisins_2.append((i+k+1, j+k+1))
                voisins_2.append((i+k, j+k))
        except:
            pass

        for k in range(1,11):
            try:
                if table[i+k][j-k] != 0:
                    break
                voisins.append((i+k, j-k))
            except:
                break
        try:
            case = table[i+k][j-k]
            if (((case == 2 or case == 4) and table[i][j] == 3) or ((case == 1 or case == 3) and table[i][j] == 4)) and table[i+k+1][j-k-1] == 0:
                voisins_2.append((i+k+1, j-k-1))
                voisins_2.append((i+k, j-k))
        except:
            pass

    _voisins = voisins.copy() # on copie la liste pour éviter des problèmes en enlevant des éléments
    for v in voisins:
        if not(0 <= v[0] <= 9) or not(0 <= v[1] <= 9) or table[v[0]][v[1]] != 0: #si les coordonnées ne sont pas comprises entre 0 et 9 ou la case n'est pas vide
            _voisins.remove(v) # on enlève le couple de coordonnées

    return _voisins, voisins_2
    
# ------------------------------------------------------------------------------------------------------------------

def verifier_gain() -> bool:
    """
    Détermine si un des joueurs a gagné en vérifiant pour chacun des joueurs
    qu'aucune case énemi reste sur le plateau
    
    :return: de type bool
    """

    j1_gagne = True
    j2_gagne = True

    for ligne in table:
        for case in ligne:
            if case == 1: # pion du joueur 1
                j2_gagne = False # le joueur 2 n'as pas éliminé tout les poins adverses
            elif case == 2: # pion du joueur 2
                j1_gagne = False # le joueur 1 n'as pas éliminé tout les poins adverses

    return (j1_gagne or j2_gagne) # on cherche à savoir si un des deux a gagné sans distinction
    
    
    
# ------------------------------------------------------------------------------------------------------------------

def on_click(event):
    """
        Fonction qui s'execute à chaque fois que la souris est préssée.
        Sert à lancer la vérification de la grille e l'affichage des pions.
        
        :param event: contient les coordonnées de la souris
    """
    
    global tour, score_j1, score_j2, table, pion_selectionne, canvas

    j, i = event.x // dx, event.y // dy # on trouve les coordonnées i et j de la case cliquée

    if not(0 <= i <= 9) or not(0 <= j <= 9): # on vérifie que le joueur a bien cliqué sur le plateau
        return


    if pion_selectionne == None: # aucun pion n'est sélectionné
        if tour % 2 == 0: # tour du joueur 1
            if table[i][j] == 1 or table[i][j] == 3: # si le pion appartient au joueur 1
                pion_selectionne = [i, j]
        else: # tour du joueur 2
            if table[i][j] == 2 or table[i][j] == 4: # si le pion appartient au joueur 2
                pion_selectionne = [i, j]

    else: # un pion est déjà sélectionné

        if (i, j) in voisins(pion_selectionne[0], pion_selectionne[1])[0]: # le pion se trouve dans les cases possible
            table[i][j] = table[pion_selectionne[0]][pion_selectionne[1]]
            table[pion_selectionne[0]][pion_selectionne[1]] = 0
            pion_selectionne = None
            tour += 1

        elif (i, j) in voisins(pion_selectionne[0], pion_selectionne[1])[1]: # le pion se trouve dans les cases possible avec prise
            index_pris = voisins(pion_selectionne[0], pion_selectionne[1])[1].index((i, j)) + 1
            pris = voisins(pion_selectionne[0], pion_selectionne[1])[1][index_pris]

            table[i][j] = table[pion_selectionne[0]][pion_selectionne[1]]
            table[pion_selectionne[0]][pion_selectionne[1]] = 0

            table[pris[0]][pris[1]] = 0

            pion_selectionne = None
            tour += 1

        elif tour % 2 == 0: # tour du joueur 1 
            if table[i][j] == 1 or table[i][j] == 3:
                pion_selectionne = [i, j]
        else: # tour du joueur 2
            if table[i][j] == 2 or table[i][j] == 4: # si le pion appartient au joueur 2
                pion_selectionne = [i, j]


    # on tranforme les pions ayant atteint le bout du plateau en dame
    for j in range(10):
        if table[0][j] == 1:
            table[0][j] = 3
    for j in range(10):
        if table[9][j] == 2:
            table[9][j] = 4


    dessiner_pions()

    # vérification des gains à la fin du tour
    if verifier_gain():
        if tour % 2 == 0:
            tkinter.messagebox.showinfo(title='Gagné !', message=f'{nom_j2.get()} a gagné !')
            score_j2 += 1
            reinitialiser()
        else:
            tkinter.messagebox.showinfo(title='Gagné !', message=f'{nom_j1.get()} a gagné !')
            score_j1 += 1
            reinitialiser()


def reinitialiser():
    """
    Fonction qui réinitialise la fenêtre de jeu en detruisant la fenêtre précedente
    et en en recréant une autre.
    """
    
    global tour, table, pion_selectionne
    fenetre.destroy() # on détruit la fenêtre actuelle
    tour = 0
    pion_selectionne = None
    table = [[0 for _ in range(10)] for _ in range(10)]
    main() # on rappel la fonction 'main' afin de recréer une fenêtre


def placer_pions():
    """
    Place les pions dans leur position de départ
    """

    global table
    for i in range(4):
        for j in range((i+1) % 2, 10, 2):
            table[i][j] = 2

    for i in range(6, 10):
        for j in range((i+1) % 2, 10, 2):
            table[i][j] = 1


def dessiner_pions():
    """
    Efface le canvas et dessine tout les pions du plateau.
    Souligne aussi la case sélectionné et les cases sur lequelles il est possible de bouger.
    """

    global canvas, pion_selectionne
    canvas.delete("all")

    canvas.create_image(250, 250, image=filename) # arrière plan

    if pion_selectionne:
        i, j = pion_selectionne
        canvas.create_rectangle(j * dx, i * dy, j * dx + 50, i * dy + 50, outline='black', fill='gold') # case sélectionné
        for voisin in voisins(i, j)[0]:
            i, j = voisin
            canvas.create_rectangle(j * dx, i * dy, j * dx + 50, i * dy + 50, outline='black', fill='green2') # case où l'on peut bouger
        
        prises_possible = voisins(pion_selectionne[0], pion_selectionne[1])[1]
        if prises_possible:
            for k in range(0, len(prises_possible), 2):
                i, j = prises_possible[k]
                canvas.create_rectangle(j * dx, i * dy, j * dx + 50, i * dy + 50, outline='black', fill='red2') # case où si l'on bouge on prends un pion adverse

    for i in range(10):
        for j in range(10):
            if table[i][j] == 1:
                canvas.create_oval(j * dx, i * dy, j * dx + 50, i * dy + 50, outline='black', fill='white') # pion blanc
            elif table[i][j] == 2:
                canvas.create_oval(j * dx, i * dy, j * dx + 50, i * dy + 50, outline='white', fill='black') # pion noir
            elif table[i][j] == 3:
                canvas.create_oval(j * dx, i * dy, j * dx + 50, i * dy + 50, outline='black', fill='white')           # dame
                canvas.create_oval(j * dx + 10, i * dy + 10, j * dx + 40, i * dy + 40, outline='black', fill='black') # blanche
            elif table[i][j] == 4:
                canvas.create_oval(j * dx, i * dy, j * dx + 50, i * dy + 50, outline='white', fill='black')           # dame
                canvas.create_oval(j * dx + 10, i * dy + 10, j * dx + 40, i * dy + 40, outline='white', fill='white') # noir


def main():
    
    # initialisation de la fenêtre
    global fenetre, canvas, filename
    fenetre = Tk()
    fenetre.title("Jeu des dames")
    fenetre.geometry('504x600')
    fenetre.configure(bg='grey25')
    fenetre.resizable(width=False, height=False)

    filename = PhotoImage(file = "dame_image.png")
    
    # canvas pour dessiner
    canvas = Canvas(fenetre, width=500, height=500, highlightthickness=0)
    canvas.pack()

    placer_pions()
    dessiner_pions()

    # étiquettes de nom
    etiquette1 = Label(fenetre, text="Joueur 1:", font='Times 20 bold', bg='white', fg='black', height=1, width=8)
    etiquette1.place(x=0, y=510)

    etiquette2 = Label(fenetre, text="Joueur 2:", font='Times 20 bold', bg='black', fg='white', height=1, width=8)
    etiquette2.place(x=0, y=560)

    # Création de variables de type modifiable et gérées par tkinter
    global nom_j1, nom_j2, score
    nom_j1 = StringVar()
    nom_j2 = StringVar()
    score = StringVar()
    score.set('score : ' + str(score_j1) + ' - ' + str(score_j2))

    # Création des champs de saisie de texte
    saisie1 = Entry(fenetre, textvariable=nom_j1, bd=5)
    saisie1.place(x=140, y=515)
    saisie2 = Entry(fenetre, textvariable=nom_j2, bd=5)
    saisie2.place(x=140, y=565)
    
    # étiquette de score
    etiquette3 = Label(fenetre, textvariable=score, font='Times 20 bold', bg='grey25', fg='white', height=1, width=8)
    etiquette3.place(x=320, y=535)

    # linkage du bouton gauche de la souris avec la fonction 'on_click'
    # pour appeler cette fonction à chaque fois que la souris est pressée
    fenetre.bind("<Button-1>", on_click)
    fenetre.mainloop()


if __name__ == '__main__':
    main()