from abr import *
from parcours import *
  
def tri_par_ABR(liste):
    """ Fonction qui retourne la liste triée à l'aide d'un ABR """
    e = liste[0]
    abr = ABR(e)
    for e in liste[1:]:
        abr.inserer(e)
    return infixe(abr)