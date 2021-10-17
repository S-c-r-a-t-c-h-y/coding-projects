from collections import deque


class File:
    """Classe modélisant une File
    On considère que la file va de gauche (fin) à droite (tête)
    """
    # Constructeur
    def __init__(self, iterable=None):
        if iterable is None:
            iterable = []
        self.__elements = deque(iterable)
        
    def est_vide(self):
        return len(self.__elements) == 0
    
    def sommet(self):
        return self.__elements[-1]
    
    def enfiler(self, e):
        self.__elements.appendleft(e)
    
    def defiler(self):
        return self.__elements.pop()
    
    def afficher(self):
        print(self.__elements)
        
    def __str__(self):
        return f'{self.__elements}'