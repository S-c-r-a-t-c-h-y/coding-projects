def maxi(tab):
    if not tab:
        return None
    maximum = tab[0]
    index = 0
    for i, nombre in enumerate(tab):
        if nombre > maximum:
            maximum = nombre
            index = i
    return maximum, index


# print(maxi([1, 5, 6, 9, 1, 2, 3, 7, 9, 8]))


def recherche(gene, seq_adn):
    n = len(seq_adn)
    g = len(gene)
    i = 0
    trouve = False
    while i < n - g and trouve == False:
        j = 0
        while j < g and gene[j] == seq_adn[i + j]:
            j += 1
        if j == g:
            trouve = True
        i += 1
    return trouve


print(recherche("AATC", "GTACAAATCTTGCC"))
print(recherche("AGTC", "GTACAAATCTTGCC"))
