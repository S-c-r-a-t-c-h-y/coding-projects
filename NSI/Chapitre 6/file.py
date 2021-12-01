from collections import deque

class File:
    """Classe modélisant une File
    On considère que la file va de gauche (fin) à droite (tête)
    """
    # Constructeur
    def __init__(self):
        self.__elements = deque()
        
    def est_vide(self):
        return len(self.__elements) == 0
    
    def sommet(self):
        return self.__elements[-1]
    
    def enfiler(self, e):
        self.__elements.appendleft(e)
    
    def defiler(self):
        return self.__elements.pop()
    
    def __repr__(self):
        """ Surcharge de la fonction print() """
        return str(self.__elements)  