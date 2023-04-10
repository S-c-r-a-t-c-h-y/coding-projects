def recherche(elt, tab):
    for i, elem in enumerate(tab):
        if elem == elt:
            return i
    return -1


# print(recherche(1, [2, 3, 4]))
# print(recherche(1, [10, 12, 1, 56]))
# print(recherche(50, [1, 50, 1]))


def insere(a, tab):
    l = list(tab)  # l contient les mêmes éléments que tab
    l.append(a)
    i = len(tab) - 1
    while a < l[i] and i >= 0:
        l[i + 1] = tab[i]
        l[i] = a
        i -= 1
    return l


# print(insere(3, [1, 2, 4, 5]))
# print(insere(10, [1, 2, 7, 12, 14, 25]))
