def recherche(liste):
    if len(liste) <= 1:
        return []
    consecutif = []
    for i in range(1, len(liste)):
        if liste[i - 1] == liste[i] - 1:
            consecutif.append((liste[i - 1], liste[i]))
    return consecutif


# print(recherche([1, 4, 3, 5]))
# print(recherche([1, 4, 5, 3]))


def propager(M, i, j, val):
    if M[i][j] == 0:
        return

    M[i][j] = val

    # l'élément en haut fait partie de la composante
    if (i - 1) >= 0 and M[i - 1][j] == 1:
        propager(M, i - 1, j, val)

    # l'élément en bas fait partie de la composante
    if (i + 1) < len(M) and M[i + 1][j] == 1:
        propager(M, i + 1, j, val)

    # l'élément à gauche fait partie de la composante
    if (j - 1) >= 0 and M[i][j - 1] == 1:
        propager(M, i, j - 1, val)

    # l'élément à droite fait partie de la composante
    if (j + 1) < len(M) and M[i][j + 1] == 1:
        propager(M, i, j + 1, val)


m = [[0, 0, 1, 0], [0, 1, 0, 1], [1, 1, 1, 0], [0, 1, 1, 0]]
propager(m, 2, 1, 3)
# print(m)
