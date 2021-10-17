from pile import Pile


class File:
    """Classe modélisant une File
    On considère que la file va de gauche (fin) à droite (tête)
    """
    # Constructeur
    def __init__(self):
        self.__pe = Pile()
        self.__ps = Pile()
        
    def est_vide(self):
        return len(self.__pe) == 0 and len(self.__ps) == 0
    
    def sommet(self):
        return self.__ps.sommet()
    
    def enfiler(self, e):
        self.__pe.empiler(e)
    
    def defiler(self):
        if self.__ps.est_vide():
            while not(self.__pe.est_vide()):
                self.__ps.empiler(self.__pe.depiler())
        return self.__ps.depiler()
    
    def afficher(self):
        self.__pe.afficher()
        self.__ps.afficher()
        
        
file1 = File()
for i in range(6):
    file1.enfiler(i)
file1.defiler()
for i in range(6,11):
    file1.enfiler(i)
file1.defiler()
file1.afficher()