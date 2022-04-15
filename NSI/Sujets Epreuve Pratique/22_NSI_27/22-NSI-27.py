def taille(arbre, lettre):
    if arbre[lettre] == ["", ""]:
        return 1
    if arbre[lettre][0] == "":
        return 1 + taille(arbre, arbre[lettre][1])
    if arbre[lettre][1] == "":
        return 1 + taille(arbre, arbre[lettre][0])
    return 1 + taille(arbre, arbre[lettre][0]) + taille(arbre, arbre[lettre][1])


a = {"F": ["B", "G"], "B": ["A", "D"], "A": ["", ""], "D": ["C", "E"], "C": ["", ""], "E": ["", ""], "G": ["", "I"], "I": ["", "H"], "H": ["", ""]}

# print(taille(a, "F"))


def tri_iteratif(tab):
    for k in range(len(tab) - 1, 0, -1):
        imax = k
        for i in range(0, k):
            if tab[i] > tab[imax]:
                imax = i
        if tab[imax] > tab[k]:
            tab[k], tab[imax] = tab[imax], tab[k]
    return tab


# print(tri_iteratif([41, 55, 21, 18, 12, 6, 25]))
