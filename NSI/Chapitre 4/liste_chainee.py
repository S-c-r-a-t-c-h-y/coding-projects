class Maillon:
    """ Classe modélisant un maillon d'une liste chaînée """
     # Constructeur
    def __init__(self, v = None, s = None):
        self.__valeur = v
        self.__suivant = s
        
    # Accesseurs
    def get_valeur(self):
        return self.__valeur
    
    def get_suivant(self):
        return self.__suivant
    
    # Mutateurs
    def set_valeur(self, v):
        self.__valeur = v
        
    def set_suivant(self, m):
        self.__suivant = m
       
       
class Liste_chainee:
    """ classe modélisant une liste chaînée """
    def __init__(self):
        self.__tete = None
    
    def get_tete(self):
        return self.__tete
    
    def set_tete(self, tete):
        self.__tete = tete
    
    def est_vide(self):
        return self.__tete is None
    
    def placer(self, v, n=1):
        
        if self.get_tete() is None:
            self.set_tete(Maillon(v))
            return

        if n == 1:
            self.set_tete(Maillon(v, self.get_tete()))
            return

        maillon = self.get_tete()

        for _ in range(n-2):
            suivant = maillon.get_suivant()
            if suivant is not None:
                maillon = suivant
            else:
                break

        suivant = maillon.get_suivant()
        nouveau_maillon = Maillon(v) if suivant is None else Maillon(v, suivant)
        maillon.set_suivant(nouveau_maillon)
        
    def placer_fin(self, v):
        
        maillon = self.get_tete()
        while (suivant := maillon.get_suivant()) is not None:
            maillon = suivant
        maillon.set_suivant(Maillon(v))
        
    def enlever(self):
        nouvelle_tete = self.get_tete().get_suivant()
        self.set_tete(nouvelle_tete)
        
    def index(self, v):
        if v not in self:
            raise IndexError(f"La liste chainée ne contient pas l'élément {v}.")
        
        index = 0
        maillon = self.get_tete()
        while maillon is not None:
            if maillon.get_valeur() == v:
                return index
            maillon = maillon.get_suivant()
            index += 1
        
    def __repr__(self) :
        """ surcharge de la fonction print """
        m = self.__tete
        chaine = ''
        while m != None:
            chaine = f'{chaine} -> {m.get_valeur()}'
            m = m.get_suivant()
        return chaine
    
    def __len__(self):
        _len = 0
        maillon = self.get_tete()
        while maillon is not None:
            _len += 1
            maillon = maillon.get_suivant()
        return _len
    
    def __contains__(self, v):
        trouve = False
        maillon = self.get_tete()
        while maillon is not None:
            if maillon.get_valeur() == v:
                trouve = True
            maillon = maillon.get_suivant()
        return trouve
        
        
        