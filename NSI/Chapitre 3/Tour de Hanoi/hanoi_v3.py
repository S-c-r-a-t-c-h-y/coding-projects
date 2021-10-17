# MAZOYER AMAURY TE

# TOUR DE HANOI AVEC INTERFACE GRAPHIQUE TKINTER
# TECHNIQUE D'AFFICHAGE UTILISE : UN OBJET PAR
# DISQUE, DEPLACEMENT DE L'OBJECT DISQUE COMME MOUVEMENT

from pile import Pile
import tkinter as tk
from numpy import interp
import random
import time

class Hanoi(tk.Tk):
    """ classe qui gère l'entièreté des tours de hanoi
        (affichage et résolution)
        Elle hérite de tk.Tk et se comporte comme un fenêtre qu'on
        aurait instancié avec tk.Tk()        
        """
    def __init__(self, nb_disques=3):
        
        # stock les rectangle qui servent de disques en mémoire
        self.disques = {}
        
        ### variables qui structures les tours de hanoi ###
        self.__pile1 = Pile([i for i in range(nb_disques, 0, -1)])
        self.__pile2 = Pile()
        self.__pile3 = Pile()
        self.__tours = [self.__pile1, self.__pile2, self.__pile3]
        self.__nb_disques = nb_disques
        
        # permet de connaitre les derniers points de départ et d'arrivé afin de pouvoir
        # les échanger et relancer l'algorithme plusieurs fois
        self.tour_depart = 1
        self.tour_arrive = 3
        
        ### INTERFACE GRAPHIQUE TKINTER ###
        tk.Tk.__init__(self)
        self.WIDTH = 660
        self.TOWER_WIDTH = self.WIDTH/3 - 50
        self.MIN_WIDTH = 40
        
        self.EPAISSEUR_DISQUE = 40
        
        self.HEIGHT = (self.__nb_disques + 2) * self.EPAISSEUR_DISQUE
        self.DST_HAUT = self.EPAISSEUR_DISQUE
        
        # liste de nb_disques couleurs aléatoires
        self.COLORS = [self.rgb_to_hex(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(nb_disques)]
        
        self.INTERVALLE_TEMPS = 0.0
        
        self.title("Tours de Hanoi")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(width=False, height=False)
        
        self.canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg='white')
        self.canvas.place(x=0, y=0)
        
        self.dessiner_supports()
        self.creer_disques()
        
        self.bind('<Return>', self.appeler_hanoi)

        self.mainloop()
        
    def creer_disques(self):
        """ créer les rectangles qui servent de disques et les ajoute au dict self.disques """
        pile1 = self.__pile1.to_list()
        for i, disque in enumerate(pile1):
            couleur = self.COLORS[disque-1]
            
            self.disques[disque] = self.dessiner_disque(0, i, disque, couleur)
        
    def dessiner_supports(self):
        """ méthode qui dessine les 3 piliers des tours sur le canvas"""
        EPAISSEUR = 10
        for i in range(1, 6, 2):
            self.canvas.create_rectangle((self.WIDTH/6) * i - EPAISSEUR/2, self.DST_HAUT, (self.WIDTH/6) * i + EPAISSEUR/2, self.HEIGHT, fill='brown')
            
    def rgb_to_hex(self, r, g, b):
        """ méthode qui transforme un couple couleur rgb en sa valeur hexadécimal"""
        return f'#{r:02x}{g:02x}{b:02x}'
        
    def dessiner_disque(self, tour: int, nb_hauteur: int, disque, couleur: str):
        """ dessine sur le canvas un disque de couleur "couleu"r sur la tour n°"tour" à la "nb_hauteur"ème place en hauteur dans la pile
            avec une largeur de "largeur" et une hauteur de "hauteur".
            Retourne le rectangle qui sert de disque
            """
        
        x1, y1, x2, y2 = self.get_coords(tour, nb_hauteur, disque)
        
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill=couleur)

    def deplacer(self, depart: int, arrive: int):
        """ deplace l'object du dessus de la pile n°depart vers la pile n°arrivé """
        obj = self.__tours[depart-1].depiler()
        self.__tours[arrive-1].empiler(obj)
        
        disque = self.disques[obj]
        x1, y1, x2, y2 = self.get_coords(arrive-1, len(self.__tours[arrive-1])-1, obj)
        
        self.canvas.coords(disque, x1, y1, x2, y2)
        self.update()
        
    def get_coords(self, tour: int, nb_hauteur: int, disque: int):
        """ obtient les coordonnées d'un rectangle en fonction de la pile dans laquelle
            il se trouve, de la hauteur où il se trouve dans la pile et de sa valeur """
        
        largeur = interp(disque, [1, self.__nb_disques], [self.MIN_WIDTH, self.TOWER_WIDTH])
        width6 = self.WIDTH/6 # un sixième de la largeur de la fenêtre
        
        # coin inférieur gauche
        x1 = width6 + width6 * tour * 2 - largeur/2
        y1 = self.HEIGHT - (self.EPAISSEUR_DISQUE * nb_hauteur) - self.EPAISSEUR_DISQUE
        
        x2 = width6 + width6 * tour * 2 + largeur/2
        y2 = y1 + self.EPAISSEUR_DISQUE
        
        return x1, y1, x2, y2
        
    def appeler_hanoi(self, event):
        """ méthode qui appele la méthode hanoi
            cette méthode est nécessaire pour que la méthode
            hanoi soit compatible avec tkinter """
        
        self.hanoi()
        self.tour_depart, self.tour_arrive = self.tour_arrive, self.tour_depart
    
    def hanoi(self, n=None, tour_depart: int = 0, tour_arrive: int = 0, tour_intermediaire: int = 2):
        """ méthode qui permet de déplacer le contenu de la tour de départ
            vers la tour d'arrivée dans le même ordre et sans jamais
            superposer un disque avec une valeur plus élevée que celui du dessous
            
            :param n: nombre de disque à déplacer
            """
        
        # permet de lancer la fonction sans passer d'arguments
        if n is None:
            n = self.__nb_disques
        
        if tour_depart == 0:
            tour_depart = self.tour_depart
        if tour_arrive == 0:
            tour_arrive = self.tour_arrive
        
        if n != 0:
            self.hanoi(n-1, tour_depart, tour_intermediaire, tour_arrive)
            self.deplacer(tour_depart, tour_arrive)
            time.sleep(self.INTERVALLE_TEMPS)
            self.hanoi(n-1, tour_intermediaire, tour_arrive, tour_depart)

    def afficher_piles(self):
        """ affiche l'état actuel des piles dans la console """
        
        print(f"Pile 1 : {self.__pile1}\nPile 2 : {self.__pile2}\nPile 3 : {self.__pile3}\n")

        
if __name__ == '__main__':
    nb_disques = 10
    hanoi = Hanoi(nb_disques)
