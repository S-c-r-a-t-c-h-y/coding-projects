from arbre_binaire import AB
from file import File
from dessiner_arbre import dessiner

        
def largeur(arbre):
    """ Fonction qui retourne le parcours en largeur de l'arbre
        sous la forme d'une liste
    """
    liste = []
    if arbre != None:
        f1 = File()
        f1.enfiler(arbre)
        while f1.est_vide() == False:
            pass
    return liste


arbre1 = AB(2, AB(3), AB(8))
arbre2 = AB(8, AB(5, AB(1), AB(2)), AB(7))
arbre3 = AB(5, AB(4, AB(2), AB(3)), AB(8, AB(9), AB(1)))