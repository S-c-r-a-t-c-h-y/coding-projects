from pile import Pile


def insertion(e, p) :
    """ Fonction qui insère un élément e dans une pile p triée dans l'ordre décroissant"""
    p1 = Pile()
    
    trouve = False
    while not(p.est_vide()):
        elem = p.depiler()
        if elem >= e and not trouve:
            p1.empiler(e)
            trouve = True
        p1.empiler(elem)
            
    while not(p1.est_vide()):
        p.empiler(p1.depiler())

        
        
pile1 = Pile()
for i in range(20, -2, -2):
    pile1.empiler(i)
print('Contenu de la pile avant insertion : ')
pile1.afficher()
print('')
insertion(7, pile1)
print('Contenu de la pile après insertion : ')
pile1.afficher()


