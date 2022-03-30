class Pile:
    """Classe modélisant une Pile"""

    # Constructeur
    def __init__(self):
        self.__elements = []

    def empiler(self, e):
        self.__elements.append(e)

    def est_vide(self):
        return len(self.__elements) == 0

    def sommet(self):
        if not self.est_vide():
            return self.__elements[-1]

    def depiler(self):
        if not self.est_vide():
            return self.__elements.pop()

    def __repr__(self):
        """Surcharge de la fonction print()"""
        return str(self.__elements)
