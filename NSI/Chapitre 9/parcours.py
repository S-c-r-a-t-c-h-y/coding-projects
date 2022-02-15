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
        liste += prefixe(arbre.get_ad())
    return liste
        
def infixe(arbre):
    """ Fonction qui retourne le parcours infixe de l'arbre
        sous la forme d'une liste
    """
    liste = []
    if arbre != None:
        liste += infixe(arbre.get_ag())
        liste.append(arbre.get_val())
        liste += infixe(arbre.get_ad())
    return liste

def postfixe(arbre):
    """ Fonction qui retourne le parcours postfixe de l'arbre
        sous la forme d'une liste
    """
    liste = []
    if arbre != None:
        liste += postfixe(arbre.get_ag())
        liste += postfixe(arbre.get_ad())
        liste.append(arbre.get_val())
    return liste
      
      
arbre1 = AB(5, AB(2), AB(1))
arbre2 = AB(8, AB(5, AB(1), AB(2)), AB(7))
arbre3 = AB(5, AB(4, AB(2), AB(3)), AB(8, AB(9), AB(1)))