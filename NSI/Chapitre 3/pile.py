class Pile:
    """Classe modélisant une Pile"""
    # Constructeur
    def __init__(self, iterable=None):
        if iterable is None:
            iterable = []
        self.__elements = list(iterable)
        
    def est_vide(self):
        return len(self.__elements) == 0
    
    def sommet(self):
        return self.__elements[-1]
    
    def empiler(self, e):
        self.__elements.append(e)
    
    def depiler(self):
        return self.__elements.pop()
    
    def afficher(self):
        print(self.__elements)
        
    def __str__(self):
        return f'{self.__elements}'