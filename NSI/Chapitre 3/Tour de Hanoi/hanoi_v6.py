# MAZOYER AMAURY TE

# TOUR DE HANOI AVEC INTERFACE GRAPHIQUE TKINTER
# TECHNIQUE D'AFFICHAGE UTILISE : UN OBJET PAR
# DISQUE, DEPLACEMENT DE L'OBJECT DISQUE COMME MOUVEMENT

# JOUEUR SELECTIONNE ET BOUGE LES DISQUES LUI MEME
# LE MOUVEMENT DES DIQUES EST ANIME

from pile import Pile
import tkinter as tk
import tkinter.messagebox
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
        
        ### INTERFACE GRAPHIQUE TKINTER ###
        tk.Tk.__init__(self)
        self.STEPS = 20
        self.WIDTH = 660
        self.TOWER_WIDTH = self.WIDTH/3 - 50
        self.MIN_WIDTH = 40
        
        self.EPAISSEUR_DISQUE = 40
        
        self.HEIGHT = (self.__nb_disques + 2) * self.EPAISSEUR_DISQUE
        self.DST_HAUT = self.EPAISSEUR_DISQUE
        
        self.COORDS_HAUT = [self.WIDTH/6 * (i*2+1) for i in range(3)]
        
        # liste de nb_disques couleurs aléatoires
        self.COLORS = [self.rgb_to_hex(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(nb_disques)]
        
        # temps que prend le déplacement à se réalise
        self.INTERVALLE_TEMPS = 0.5
        
        self.title("Tours de Hanoi")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.resizable(width=False, height=False)
        
        self.canvas = tk.Canvas(self, width=self.WIDTH, height=self.HEIGHT, bg='white')
        self.canvas.place(x=0, y=0)
        
        self.dessiner_supports()
        self.creer_disques()
        
        ### AUTRE ###
        self.selectionne = None
        self.start_time = time.time()
        
        self.bind('<Button-1>', self.select)

        self.mainloop()
    
    def select(self, event):
        x, y = event.x, event.y
        closest = self.canvas.find_closest(x, y)[0]
        
        tour = int(x // (self.WIDTH/3) + 1)
        
        disque = int(interp(closest, [4, self.__nb_disques+3], [self.__nb_disques, 1]))

        x1, _, x2, _ = self.get_coords(tour-1, len(self.__tours[tour-1]), disque)
        y = interp(y, [0, self.HEIGHT], [self.HEIGHT, 0])

        try:
            hauteur_disque = self.__tours[tour-1].to_list().index(disque)
        except ValueError:
            hauteur_disque = -1
    
        if not self.selectionne:
            if x1 <= x <= x2 and hauteur_disque * self.EPAISSEUR_DISQUE <= y <= (hauteur_disque + 1) * self.EPAISSEUR_DISQUE :
                if (sommet := self.__tours[tour-1].sommet()) is not None and sommet == disque:
                    self.selectionne = (sommet, tour)
                    self.canvas.itemconfigure(self.disques[sommet], fill='red')
        else:
            disque = self.selectionne[0]
            if (sommet := self.__tours[tour-1].sommet()) is None or sommet > disque:
                self.deplacer(self.selectionne[1], tour)
                self.canvas.itemconfigure(self.disques[disque], fill=self.COLORS[disque-1])
                
            elif tour == self.selectionne[1]:
                sommet = self.selectionne[0]
                self.canvas.itemconfigure(self.disques[sommet], fill=self.COLORS[sommet-1])
                self.selectionne = None
        
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
        d_temps = (self.INTERVALLE_TEMPS / 3) / self.STEPS
        
        _, y1, _, _ = self.canvas.coords(disque)
        dy = -y1
        
        for _ in range(self.STEPS):
            self.canvas.move(disque, 0, dy/self.STEPS)
            self.update()
            time.sleep(d_temps)
        
        x2 = self.COORDS_HAUT[depart-1]
        x3 = self.COORDS_HAUT[arrive-1]
        dx = x3-x2
        
        for _ in range(self.STEPS):
            self.canvas.move(disque, dx/self.STEPS, 0)
            self.update()
            time.sleep(d_temps)
        
        _, y1, _, _ = self.get_coords(arrive-1, len(self.__tours[arrive-1])-1, obj)
        dy = y1
        for _ in range(self.STEPS):
            self.canvas.move(disque, 0, dy/self.STEPS)
            self.update()
            time.sleep(d_temps)
        
        if self.__tours[2].to_list() == [i for i in range(self.__nb_disques, 0, -1)]:
            tkinter.messagebox.showinfo(title="Vous avez réussi !", message=f"Vous avez déplacé tout les disques vers la tour d'arrivé avec succès en {time.time() - self.start_time:.2f}s.")
            self.destroy()
        
        self.update()
        self.selectionne = None
        
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

    def afficher_piles(self):
        """ affiche l'état actuel des piles dans la console """
        
        print(f"Pile 1 : {self.__pile1}\nPile 2 : {self.__pile2}\nPile 3 : {self.__pile3}\n")

        
if __name__ == '__main__':
    nb_disques = 4
    hanoi = Hanoi(nb_disques)
