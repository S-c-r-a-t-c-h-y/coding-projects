from file import File
from random import randint


def maximum(f) :
    """ Fonction qui retourne le maximum de la file f"""
    f1 = File()
    m = float('-inf')
    
    while not(f.est_vide()):
        e = f.defiler()
        f1.enfiler(e)
        if e >= m:
            m = e
            
    while not(f1.est_vide()):
        f.enfiler(f1.defiler())
        
    return m
        
file1 = File()
for i in range(11):
    file1.enfiler(randint(0,100))
print('Contenu de la file avant recherche : ')
file1.afficher()
print('')
print("Maximum de la file : ")
print(maximum(file1))
print('')
print('Contenu de la file après recherche : ')
file1.afficher()


