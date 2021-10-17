from pile import Pile

class Hanoi:
    
    def __init__(self, nb_disques=3):
        self.__pile1 = Pile([i for i in range(nb_disques, 0, -1)])
        self.__pile2 = Pile()
        self.__pile3 = Pile()
        self.__tours = [self.__pile1, self.__pile2, self.__pile3]
        self.__nb_disques = nb_disques
        
    def deplacer(self, depart: int, arrive: int):
        """ deplace l'object du dessus de la pile n°depart vers l pile n°arrivé """
        self.__tours[arrive-1].empiler(self.__tours[depart-1].depiler())
        print(self)
        
    def sommet(self, tour):
        """ retourne le sommet de la tour n°tour"""
        return self.__tours[tour-1]
    
    def hanoi(self, n=None, tour_depart: int = 1, tour_arrive: int = 3, tour_intermediaire: int = 2):
        """ méthode qui permet de déplacer le contenu de la tour de départ
            vers la tour d'arrivée dans le même ordre et sans jamais
            superposer un disque avec une valeur plus élevée que celui du dessous
            
            :param n: nombre de disque à déplacer
            """
        
        if n is None:
            n = self.__nb_disques
        
        if n != 0:
            self.hanoi(n-1, tour_depart, tour_intermediaire, tour_arrive)
            self.deplacer(tour_depart, tour_arrive)
            self.hanoi(n-1, tour_intermediaire, tour_arrive, tour_depart)
            
    
    def __repr__(self):
        return f"Pile 1 : {self.__pile1}\nPile 2 : {self.__pile2}\nPile 3 : {self.__pile3}\n"

        
if __name__ == '__main__':
    nb_disques = 4
    h = Hanoi(nb_disques)
    print(h)
    h.hanoi()
