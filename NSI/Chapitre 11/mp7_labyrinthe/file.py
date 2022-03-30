from collections import deque


class File:
    """Classe modélisant une File
    On considère que la file va de gauche (fin) à droite (tête)
    """
    # Constructeur
    def __init__(self):
        self.__elements = deque()
        
    def enfiler(self, e):
        self.__elements.appendleft(e)
        
    def est_vide(self):
        return len(self.__elements) == 0
    
    def defiler(self):
        if not self.est_vide():
            return self.__elements.pop()
        
    def tete(self):
        if not self.est_vide():
            return self.__elements[0]
    
    def __repr__(self):
        """ Surcharge de la fonction print() """
        return str(self.__elements)  