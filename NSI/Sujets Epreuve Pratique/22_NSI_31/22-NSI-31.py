def recherche(a, t):
    occurences = 0
    for nbr in t:
        if nbr == a:
            occurences += 1
    return occurences


# print(recherche(5,[]))
# print(recherche(5,[-2, 3, 4, 8]))
# print(recherche(5,[-2, 3, 1, 5, 3, 7, 4]))
# print(recherche(5,[-2, 5, 3, 5, 4, 5]))


def rendu_monnaie_centimes(s_due, s_versee):
    pieces = [1, 2, 5, 10, 20, 50, 100, 200]
    rendu = []
    a_rendre = s_versee - s_due
    i = len(pieces) - 1
    while a_rendre > 0:
        if pieces[i] <= a_rendre:
            rendu.append(pieces[i])
            a_rendre -= pieces[i]
        else:
            i -= 1
    return rendu


print(rendu_monnaie_centimes(700,700))
print(rendu_monnaie_centimes(112,500))