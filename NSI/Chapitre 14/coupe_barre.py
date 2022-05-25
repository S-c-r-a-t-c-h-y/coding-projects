from random import randint, seed
from sys import setrecursionlimit

setrecursionlimit(10000)
seed(15)

def genere_prix(n):
    return sorted([0] + [2 * (i + 1) + int((n - i) * i * 0.25) + randint(0, 4) for i in range(n)])

prix = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30, 36, 39, 40, 42, 42, 44, 45, 46, 47, 49, 50, 50, 51, 52, 53, 53, 54,55, 55, 55, 56, 56, 57, 57, 58, 58, 58, 58, 59, 60]
# prix = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]

def rentabilite(l):
    return prix[l] / l if l != 0 else 0

def longueur_gain_max(longueur):
    return max(((i, rentabilite(i)) for i in range(min(longueur+1, len(prix)))), key=lambda x: x[1])[0]

def coupe_glouton(longueur):
    gain = 0
    while longueur > 0:
        longueur_coupe = longueur_gain_max(longueur)
        gain += prix[longueur_coupe]
        longueur -= longueur_coupe
    return gain


def coupe_r(longueur):
    if longueur == 0:
        return 0
    vmax = -1
    for i in range(1, longueur+1):
        vmax = max(vmax, prix[i] + coupe_r(longueur-i))
    return vmax

coupes = [0] + [-1] * 10000
def coupe_memo(longueur):
    if coupes[longueur] != -1:
        return coupes[longueur]
    vmax = -1
    for i in range(1, longueur+1):
        vmax = max(vmax, prix[i] + coupe_memo(longueur-i))
    coupes[longueur] = vmax
    return vmax

def coupe_ascendante(longueur):
    tableau = [0] + [-1] * longueur
    for j in range(1, longueur+1):
        vmax = -1
        for i in range(1, j+1):
            vmax = max(vmax, prix[i] + tableau[j-i])
        tableau[j] = vmax
    return tableau[longueur]

def coupe_ascendante_solution(longueur):
    tableau = [0] + [-1] * longueur
    coupure = [0] * (longueur + 1)
    for j in range(1, longueur+1):
        vmax = -1
        for i in range(1, j+1):
            if (nouveau_prix := prix[i] + tableau[j-i]) > vmax:
                vmax = nouveau_prix
                coupure[j] = i
        tableau[j] = vmax
    return tableau, coupure

def affiche_solution(longueur):
    t, c = coupe_ascendante_solution(longueur)
    v = t[longueur]
    print(f"Solution optimale pour une barre de longueur {longueur} : ", end='')
    while longueur > 0:
        print(c[longueur], end=' ')
        longueur -= c[longueur]
    print(f"pour un total de {v}€")

# print(coupe_memo(3000))
# print(coupe_ascendante(8))
# print(coupe_ascendante(23))
# print(coupe_ascendante(40))
# prix = genere_prix(20000)
# print(coupe_ascendante(100))
# print(coupe_ascendante(10000)) # 11s
# print(coupe_ascendante(20000)) # 44s

affiche_solution(4)
affiche_solution(23)
affiche_solution(40)