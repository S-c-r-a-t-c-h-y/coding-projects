from file import File


def insertion(e, f) :
    """ Fonction qui insère un élément e dans une file f triée dans l'ordre décroissant"""
    f1 = File()
    
    trouve = False
    while not(f.est_vide()):
        elem = f.defiler()
        if elem >= e and not trouve:
            f1.enfiler(e)
            trouve = True
        f1.enfiler(elem)
            
    while not(f1.est_vide()):
        f.enfiler(f1.defiler())

        
        
file1 = File()
for i in range(0, 22, 2):
    file1.enfiler(i)
print('Contenu de la file avant insertion : ')
file1.afficher()
print('')
insertion(7, file1)
print('Contenu de la file après insertion : ')
file1.afficher()

