def occurence_max(chaine):
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o,", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    occurences = [0] * 26
    for lettre in chaine:
        if lettre in alphabet:
            occurences[alphabet.index(lettre)] += 1
    indice_max = 0
    for i in range(len(occurences)):
        if occurences[i] > occurences[indice_max]:
            indice_max = i
    return alphabet[indice_max]


ch = "je suis en terminale et je passe le bac et je souhaite poursuivre des etudes pour devenir expert en informatique"
# print(occurence_max(ch))


def nbLig(image):
    """renvoie le nombre de lignes de l'image"""
    return len(image)


def nbCol(image):
    """renvoie la largeur de l'image"""
    return len(image[0])


def negatif(image):
    """renvoie le negatif de l'image sous la forme
    d'une liste de listes"""

    # on cree une image de 0 aux memes dimensions que le parametre image
    L = [[0 for k in range(nbCol(image))] for i in range(nbLig(image))]

    for i in range(len(image)):
        for j in range(len(image[i])):
            L[i][j] = 255 - image[i][j]
    return L


def binaire(image, seuil):
    """renvoie une image binarisee de l'image sous la forme
    d'une liste de listes contenant des 0 si la valeur
    du pixel est strictement inferieure au seuil
    et 1 sinon"""

    # on cree une image de 0 aux memes dimensions que le parametre image
    L = [[0 for k in range(nbCol(image))] for i in range(nbLig(image))]

    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j] < seuil:
                L[i][j] = 0
            else:
                L[i][j] = 1
    return L


img = [
    [20, 34, 254, 145, 6],
    [23, 124, 237, 225, 69],
    [197, 174, 207, 25, 87],
    [255, 0, 24, 197, 189],
]
print(nbLig(img))
print(nbCol(img))
print(negatif(img))
print(binaire(img, 120))
