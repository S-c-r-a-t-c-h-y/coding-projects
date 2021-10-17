from pile import Pile
from random import randint


def maximum(p) :
    """ Fonction qui retourne le maximum de la pile p"""
    p1 = Pile()
    m = float('-inf')
    
    while not(p.est_vide()):
        e = p.depiler()
        p1.empiler(e)
        if e >= m:
            m = e
            
    while not(p1.est_vide()):
        p.empiler(p1.depiler())
        
    return m
        
pile1 = Pile()
for i in range(11):
    pile1.empiler(randint(0,100))
print('Contenu de la pile avant recherche : ')
pile1.afficher()
print('')
print("Maximum de la pile : ")
print(maximum(pile1))
print('')
print('Contenu de la pile après recherche : ')
pile1.afficher()

