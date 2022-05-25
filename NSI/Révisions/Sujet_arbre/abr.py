class ar:
    """Classe modélisant un arbre binaire de compétition"""
    
    # Constructeur
    def __init__(self, racine=None, gauche=None, droit=None):
        self.racine = racine
        self.gauche = gauche
        self.droit = droit
        
def racine(arb):
    return arb.racine

def gauche(arb):
    return arb.gauche

def droit(arb):
    return arb.droit

def est_vide(arb):
    return arb == None

def vainqueur(arb):
    return racine(arb)
        
def finale(arb):
    return [racine(gauche(arb)), racine(droit(arb))]

def occurrence(arb, nom):
    occurences = 0
    if racine(arb) == nom:
        occurences += 1
    if not est_vide(gauche(arb)):
        occurences += occurrence(gauche(arb), nom)
    if not est_vide(droit(arb)):
        occurences += occurrence(droit(arb), nom)
    return occurences

def a_gagne(arb, nom):
    return occurrence(arb, nom) >= 2

def nombre_matchs(arb, nom):
    if nom == racine(arb):
        return occurrence(arb, nom) - 1
    return occurrence(arb, nom)

def liste_joueurs(arb):
    if est_vide(arb):
        return []
    elif est_vide(gauche(arb)) and est_vide(droit(arb)):
        return [racine(arb)]
    else:
        return liste_joueurs(gauche(arb)) + liste_joueurs(droit(arb))

B = ar('Lea', ar('Lea', ar('Lea', ar('Marc'), ar('Lea')),
                        ar('Theo', ar('Claire'), ar('Theo'))),
              ar('Louis', ar('Louis', ar('Marie'), ar('Louis')),
                          ar('Anne', ar('Anne'), ar('Kevin'))))

print(vainqueur(B))
print(finale(B))
print(occurrence(B, "Anne"))
print(a_gagne(B, "Louis"))

print(nombre_matchs(B, "Lea"))
print(nombre_matchs(B, "Marc"))

print(liste_joueurs(B))

# 1. a) La racine est "Léa" et les valeurs de l'ensemble de feuilles sont :
# "Marc", "Lea", "Claire", "Theo", "Marie", "Louis", "Anne", "Kevin"

# 3. a) Le racine de l'arbre "Lea" compte comme un match alors que ce noeud
# ne représente pas un match, la fonction nombre_matchs(B, "Lea") renvoie donc
# 4 au lieu de 3