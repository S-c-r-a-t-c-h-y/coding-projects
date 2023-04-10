def fusion(tab1, tab2):
    i1 = 0
    i2 = 0
    tab = []
    while i1 < len(tab1) and i2 < len(tab2):
        if tab1[i1] < tab2[i2]:
            tab.append(tab1[i1])
            i1 += 1
        else:
            tab.append(tab2[i2])
            i2 += 1

    while i1 < len(tab1):
        tab.append(tab1[i1])
        i1 += 1

    while i2 < len(tab2):
        tab.append(tab2[i2])
        i2 += 1

    return tab


# print(fusion([3, 5], [2, 5]))
# print(fusion([-2, 4], [-3, 5, 10]))


def rom_to_dec(nombre):

    """Renvoie l’écriture décimale du nombre donné en chiffres romains"""

    dico = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    if len(nombre) == 1:
        return dico[nombre]

    else:
        ### on supprime le premier caractère de la chaîne contenue dans la variable nombre
        ### et cette nouvelle chaîne est enregistrée dans la variable nombre_droite
        nombre_droite = nombre[1:]

        if dico[nombre[0]] >= dico[nombre[1]]:
            return dico[nombre[0]] + rom_to_dec(nombre_droite)
        else:
            return rom_to_dec(nombre_droite) - dico[nombre[0]]


assert rom_to_dec("CXLII") == 142
