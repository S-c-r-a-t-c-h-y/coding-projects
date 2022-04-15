def moyenne(tab):
    if not tab:
        return "erreur"
    somme = 0
    for nombre in tab:
        somme += nombre
    return somme / len(tab)


# print(moyenne([5, 3, 8]))
# print(moyenne([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
# print(moyenne([]))


def tri(tab):
    # i est le premier indice de la zone non triee, j le dernier indice.
    # Au debut, la zone non triee est le tableau entier.
    i = 0
    j = len(tab) - 1
    while i != j:
        if tab[i] == 0:
            i += 1
        else:
            valeur = tab[j]
            tab[j] = tab[i]
            tab[i] = valeur
            j -= 1
    return tab


print(tri([0, 1, 0, 1, 0, 1, 0]))
