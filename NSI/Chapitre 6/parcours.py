from arbre_binaire import AB
from dessiner_arbre import dessiner


def prefixe(arbre):
    """ Fonction qui retourne le parcours prefixe de l'arbre
        sous la forme d'une liste
    """
    liste = []
    if arbre != None:
        liste.append(arbre.get_val())
        liste += prefixe(arbre.get_ag())
        pass
    

arbre1 = AB(5, AB(2), AB(1))
arbre2 = AB(8, AB(5, AB(1), AB(2)), AB(7))
arbre3 = AB(5, AB(4, AB(2), AB(3)), AB(8, AB(9), AB(1)))