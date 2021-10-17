import random
import copy
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from collections import deque
import os

BG_COLOR = 'white'

class Carte:
    """Classe modélisant une carte d'un jeux de 52 cartes"""
    
    # Attributs de classe
    liste_valeur = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'valet', 'dame', 'roi', 'as']
    liste_couleur = ['pique', 'coeur', 'carreaun', 'trèfle']
    
    # Constructeur
    def __init__(self, valeur: int, couleur: int):
        """Initialise les valeurs des attributs"""
        self.__valeur = valeur  # attribut de type int
        self.__couleur = couleur
        
    # Méthode afficher() 
    def afficher(self, numero):
        #_NB_ Le paramètre numero est loin d'être explicite, c'est en lisant
        # update_image que l'on comprend son rôle.
        
        # print(f"{Carte.liste_valeur[self.get_valeur()-2]} de {Carte.liste_couleur[self.get_couleur()-1]}")
        image = Bataille.get_card_image(self.get_valeur(), self.get_couleur())
        #_NB_ Je pense que la classe Carte devrait se contenter de retourner son image et ne pas gérer l'affichage
        Bataille.instances[0].update_image(numero, image)
        #_NB_ Cette ligne montre qu'il y a bien un problème pour afficher une carte, Bataille appelle Carte qui appelle Bataille
    
    # Accesseurs 
    def get_valeur(self):
        return self.__valeur
    def get_couleur(self):
        return self.__couleur
    
    # Mutateurs 
    def set_valeur(self, valeur):
        self.__valeur = valeur
    def set_couleur(self, couleur):
        self.__couleur = couleur
    
    # Surcharge des opérateurs de comparaison
    def __lt__(self, autre_carte):
        return self.get_valeur() < autre_carte.get_valeur()
    def __eq__(self, autre_carte):
        return self.get_valeur() == autre_carte.get_valeur()
    def __gt__(self, autre_carte):
        return self.get_valeur() > autre_carte.get_valeur()
    
    
class Jeux:
    """Classe modélisant un jeu de 52 cartes"""
    
    # Constructeur
    def __init__(self, nom, cartes):
        self.__nom = nom
        self.liste_carte = deque(cartes)
        
    # Méthode afficher()
    # def afficher(self):
    #     for carte in self.liste_carte:
    #         carte.afficher()
    
    # Méthode melanger()
    def melanger(self):
        random.shuffle(self.liste_carte)
        
    # Accesseurs
    def get_nom(self):
        return self.__nom
        
    def get_score(self):
        return len(self.liste_carte)
    
    def ajouter_cartes(self, cartes):
        self.liste_carte.extendleft(cartes)
        
        
class Bataille:
    """ classe responsable du déroulement du jeu """
    
    instances = []
    
    def __init__(self):
        """ initialisation de l'interface graphique et des joueurs """
        
        Bataille.instances.append(self)
        #_NB_ Quel est le rôle de la ligne précédente ?
        
        self.top = tk.Tk()
        self.top.title("Jeu de la bataille")
        self.top.geometry('405x340')
        self.top.configure(bg=BG_COLOR)
        self.top.resizable(width=False, height=False)
        
        self.gain = []
        self.fini = False
        self.paused = False
        self.WAITING_TIME = 1000
        
        self.jeux1, self.jeux2 = self.distribuer_jeu()

        self.scores = tk.StringVar()
        self.scores.set(f"26 - 26")
        self.label_score = tk.Label(self.top, textvariable=self.scores, font=("Arial", 30), bg=BG_COLOR, justify=tk.CENTER)
        self.label_score.pack(side=tk.TOP)
        
        self.image_j1 = None
        self.label_j1 = tk.Label(image=self.image_j1)
        self.label_j1.place(x=0, y=50)
        
        self.image_j2 = None
        self.label_j2 = tk.Label(image=self.image_j2)
        self.label_j2.place(x=200, y=50)
        
        self.top.bind("<Button-1>", self.jouer)
        self.top.mainloop()
        
    def jouer(self, event=None):
        """ fonction appelée à chaque click, elle
        est responsable de piocher les cartes et de les comparer """
        
        if self.fini: return
        if self.paused: return
        try:
            carte1 = self.jeux1.liste_carte.pop()
            carte2 = self.jeux2.liste_carte.pop()

            carte1.afficher(1)
            carte2.afficher(2)
            self.gain.extend([carte1, carte2])
            
            if carte1 > carte2:
                self.jeux1.ajouter_cartes(self.gain)
                self.gain = []
            elif carte1 < carte2:
                self.jeux2.ajouter_cartes(self.gain)
                self.gain = []
            else:
                self.paused = True
                self.gain.extend([self.jeux1.liste_carte.pop(), self.jeux2.liste_carte.pop()])
                self.label_j1.after(self.WAITING_TIME, self.set_blank_images)
                
        except IndexError: # continue jusqu'à ce qu'un des jeux soit vide et renvoi IndexError
            #_NB_ Je trouve astucieux ta gestion des batailles à répétition.
            self.afficher_score()
            self.scores.set(f"{self.jeux1.get_score()} - {self.jeux2.get_score()}")
            
    def set_blank_images(self):
        """ affiche des cartes retournées pour l'égalité et repioche
        des nouvelles cartes après un certain temps donné """
        
        image = Bataille.get_card_image(15, 1) # carte vide
        Bataille.instances[0].update_image(1, image)
        Bataille.instances[0].update_image(2, image)
        self.paused = False
        self.label_j1.after(self.WAITING_TIME, self.jouer)
        #_NB_ Il est douteux qu'une méthode qui vu son nom
        #doit afficher le dos des cartes gère aussi le rappel de la méthode jouer
    
    def afficher_score(self):
        """ méthode appelée quand un des jeux de cartes et vide,
        affiche un message avec le gagnant """
        #_NB_ J'aurais appelé cette méthode afficher_vainqueur pour plus de clareté.
        
        self.fini = True

        nom1 = self.jeux1.get_nom()
        nom2 = self.jeux2.get_nom()
        
        vainqueur = nom1 if self.jeux1.liste_carte else nom2
        
        messagebox.showinfo("Fini !", f"{vainqueur} a gagné !")
        
    def update_image(self, joueur, image):
        """ permet de configurer les labels responsables des images
        avec une nouvelle image """
        
        if joueur == 1:
            self.image_j1 = image
            self.label_j1.configure(image=self.image_j1)
            return
        self.image_j2 = image
        self.label_j2.configure(image=self.image_j2)
        
    def distribuer_jeu(self):
        """ distribue aux 2 joueurs des cartes issues du même jeu de 52 cartes
        dans un ordre aléatoire et renvoi 2 jeux """
        
        cartes = [Carte(v, c) for v in range(2, 15) for c in range(1,5)]
        random.shuffle(cartes)
        
        pt1 = cartes[:26]
        pt2 = cartes[26:]
        
        return Jeux('bob', pt1), Jeux('max', pt2)

    @staticmethod
    #_NB_ Pourquoi le programme fonctionne-t-il sans ce  @staticmethod ?

    def get_card_image(val, col):
        """ extrait l'image d'une certaine carte de la planche de 52 cartes """
        
        LONGUEUR = 142.75
        LARGEUR = 98.38
        
        cols = [4, 3, 2, 1]
        if val == 14: # cas particulier de l'as
            val = 1
        col = cols[col-1]
        
        if val == 15: # pour obtenir la carte vide
            val = 3
            col = 5
        
        X, Y = (val-1) * LARGEUR, LONGUEUR * (col-1)
        area = (X, Y, X + LARGEUR, Y + LONGUEUR)
        
        # path = "\\".join(__file__.split('\\')[:-1])
        # im = Image.open(f"{path}\\jeu_52.png")
        im = Image.open(f"jeu_52.png")
        image = im.crop(area)
        new_size = (200, 280)
        image = image.resize(new_size)

        return ImageTk.PhotoImage(image)

bataille = Bataille()