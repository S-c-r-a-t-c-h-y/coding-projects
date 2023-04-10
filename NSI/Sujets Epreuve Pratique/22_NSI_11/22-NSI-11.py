def recherche(tab, n):
    i1 = 0
    i2 = len(tab) - 1
    im = (i1 + i2) // 2
    while i1 <= i2:
        if tab[im] == n:
            return im
        if tab[im] < n:
            i1 = im + 1
        else:
            i2 = im - 1
        im = (i1 + i2) // 2
    return -1


# print(recherche([2, 3, 4, 5, 6], 5))
# print(recherche([2, 3, 4, 6, 7], 5))

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def position_alphabet(lettre):
    return ALPHABET.find(lettre)


def cesar(message, decalage):
    resultat = ""
    for lettre in message:
        if lettre in ALPHABET:
            indice = (position_alphabet(lettre) + decalage) % 26
            resultat = resultat + ALPHABET[indice]
        else:
            resultat = resultat + lettre
    return resultat


# print(cesar("BONJOUR A TOUS. VIVE LA MATIERE NSI !", 4))
# print(cesar("GTSOTZW F YTZX. ANAJ QF RFYNJWJ SXN !", -5))
