def tri_fusion(liste):
    """Fonction récursive qui trie la liste avec le tri fusion"""
    # Cas terminal
    if len(liste) <= 1:
        return liste
    # On divise la liste en deux
    milieu = len(liste) // 2
    liste1 = liste[:milieu]
    liste2 = liste[milieu:]
    # On trie chacune des deux sous-listes
    liste_triee1 = tri_fusion(liste1)
    liste_triee2 = tri_fusion(liste2)
    # On fusionne les deux sous-listes triées
    liste_triee = fusion(liste_triee1, liste_triee2)
    return liste_triee


def fusion(liste1, liste2):
    """Fonction qui fusionne deux listes triées"""
    i1 = 0
    i2 = 0
    taille1 = len(liste1)
    taille2 = len(liste2)
    liste_fusionnee = []
    while i1 < taille1 and i2 < taille2:
        if liste1[i1] < liste2[i2]:
            liste_fusionnee.append(liste1[i1])
            i1 += 1
        else:
            liste_fusionnee.append(liste2[i2])
            i2 += 1
    # Cas où toute la liste2 a déjà été rentrée dans la liste_fusionnee
    while i1 < taille1:
        liste_fusionnee.append(liste1[i1])
        i1 += 1
    # Cas où toute la liste1 a déjà été rentrée dans la liste_fusionnee
    while i2 < taille2:
        liste_fusionnee.append(liste2[i2])
        i2 += 1
    return liste_fusionnee
