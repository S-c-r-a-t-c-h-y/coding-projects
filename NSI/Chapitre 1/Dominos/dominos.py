import random

class Domino:

    def __init__(self, extremite1: int, extremite2: int):
        # non destiné à l'accès
        self.__e1 = extremite1
        self.__e2 = extremite2
        
        # variable que l'on accède
        self.__valeur = [extremite1, extremite2]
        self.public = 1
        

    def __contains__(self, val):
        return val in self.__valeur
    
    def __str__(self):
        return f"{self.__e1} | {self.__e2}"

    def __repr__(self):
        return f"Domino({self.__e1}, {self.__e2})"

    def __getattr__(self, name):
        try:
            return self.__dict__[f'_Domino__{name}']
        except KeyError:
            raise AttributeError
    
class Main:
    
    def __init__(self, dominos):
        self.__dominos = dominos
        
    def __str__(self):
        return f"{self.__dominos}"
    
    def __contains__(self, val):
        return True in [val in dom for dom in self.__dominos]
        
    
class SetDomino:
    
    def __init__(self):
        self.__dominos = sorted(list(set([tuple(sorted((i, j))) for i in range(7) for j in range(7)])))
        self.__dominos = [Domino(i, j) for i, j in self.__dominos]
        random.shuffle(self.__dominos)

    def distribuer_dominos(self, nb_joueurs):
        assert 2 <= nb_joueurs <= 4, "Le nombre de joueurs doit être compris entre 2 et 4"
        
        nb_dominos = 7 if nb_joueurs == 2 else 6
        
        jeux = [tuple([self.__dominos.pop() for _ in range(nb_dominos)]) for _ in range(nb_joueurs)]
        return jeux
        

dominos = SetDomino()
mains = dominos.distribuer_dominos(2)
main1, main2 = Main(mains[0]), Main(mains[1])

d = Domino(1, 2)
#d.test()
a = d.valeur
print(a)