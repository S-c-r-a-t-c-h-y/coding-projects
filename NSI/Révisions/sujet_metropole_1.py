### EXERCICE 1 ###

# 1. a) L'arbre possède 4 feuilles : 12, val, 21 et 32
#    b) Sous-arbre gauche du noeud 23:
#                   (19)
#                      \
#                      (21)
#    c) Cet arbre a une hauteur de 4 et une taille de 9
#    d) Les valeurs possible de val dans cet arbre sont : 16, 17

# 2. a) valeurs d'affichage du parcours infixe : 12, 13, 15, 16, 18, 19, 21, 23, 32
#    b) valeurs d'affichage du parcours infixe : 12, 13, 16, 15, 21, 19, 32, 23, 18

# 3. a)                        (18)
#                           /       \
#                          (12)     (19)
#                             \       \
#                             (13)    (21)
#                               \       \
#                               (15)    (32)
#                                 \      /
#                                 (16) (23)

# b) racine = Noeud(18)
#    racine.insere_tout([15, 13, 12, 16, 23, 19, 21, 32])
# c) bloc 3
#    bloc 2
#    bloc 1
# 4.

def recherche(self, v):
    if self.v == v:
        return True
    elif self.ag is None and self.ad is None:
        return False
    elif self.ag is None:
        return self.ad.recherche(v)
    else:
        return self.ag.recherche(v)
    
    
### EXERCICE 3 ###

# 1. Le nom générique de ces logiciels est : "Système de Gestion de Base de Données"
# 2. a) Cette instruction renvoie une erreur car elle essaye de supprimer des éléments
#       de la table train qui sont des clés étrangères de la table Reservation ce qui briserait la contrainte
#       d'intégrité référentielle.
#    b) L'insertion dans la table réservation n'est pas possible lorsque le numero de reservation est déja utilisé
# 3. a) SELECT numT FROM Train WHERE destination="Lyon";
#    b) INSERT INTO Reservation VALUES (1307, "Turing", "Alan", 33, 654);
#    c) UPDATE Train SET horaireArrivee="08:11" WHERE numT=7869;
# 4. La requête suivante permet de déterminer le nombre de réservations au nom de Grace Hopper.
# 5. SELECT destination, prix FROM Reservation
#    JOIN Train ON Reservation.numT = Train.numT
#    WHERE nomClient = "Hopper" AND prenomClient = "Grace";

def moitie_gauche(l):
    return l[:len(l)//2]
def moitie_droite(l):
    return l[len(l)//2:]

def tri_fusion(L):
    n = len(L)
    if n<=1 :
        return L
    print(L)
    mg = moitie_gauche(L)
    md = moitie_droite(L)
    L1 = tri_fusion(mg)
    L2 = tri_fusion(md)
    return fusion(L1, L2)
    

### EXERCICE 4 ###

# 1. a) Le coût du tri fusion en nombre de comparaisons est de l'ordre de O(n log n)
#    b) Le tri bulle a une complexité en O(n²), ce qui est bien moins efficace que le tri fusion.
# 2. [7, 4, 2, 1, 8, 4, 6, 3]
#    [7, 4, 2, 1]
#    [7, 4]
#    [2, 1]
#    [8, 4, 6, 3]
#    [8, 4]
#    [6, 3]
# 3.
def moitie_droite(l):
    return l[len(l)//2:]
# 4.

def fusion (L1, L2):
    L=[]
    nl=len(L1)
    n2=len(L2)
    i1=0
    i2=0  
    while i1<nl or i2<n2:
        if i1 >= nl:
            L.append(L2[i2])
            i2=i2+1
        elif i2 >= n2:
            L.append(L1[i1])
            i1 =i1+1
        else:
            e1=L1[i1]
            e2=L2[i2]
            if e1 < e2:
                L.append(e1)
                i1 += 1
            else:
                L.append(e2)
                i2 += 1
    return L

print(tri_fusion([7, 4, 2, 1, 8, 5, 6, 3]))