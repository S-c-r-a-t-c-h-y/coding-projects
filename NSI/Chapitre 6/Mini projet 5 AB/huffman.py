from arbre_binaire import AB

AB_huffman1 = AB(
    "",
    AB("", AB("E"), AB("", AB("", AB("G"), AB("A")), AB("", AB("D"), AB("L")))),
    AB("", AB("", AB("", AB("P"), AB("X")), AB("S")), AB("", AB(" "), AB("M"))),
)


def dechiffer(chaine_binaire, arbre_huffman):
    """Fonction qui permet de déchiffrer une chaine binaire en
    utilisant un arbre de Huffman."""

    chaine_retour = ""
    ab1 = arbre_huffman
    for c in chaine_binaire:
        ab1 = ab1.get_ag() if c == "1" else ab1.get_ad()
        if ab1.get_ad() is None and ab1.get_ag() is None:
            chaine_retour += ab1.get_val()
            ab1 = arbre_huffman
    return chaine_retour


def frequence(chaine):
    """Retourne un dictionnaire avec la fréquence de chaques lettres dans la chaine"""
    return {lettre: chaine.count(lettre) for lettre in sorted(set(chaine), key=lambda x: chaine.count(x))}


def arbre_huffman(dico):
    """Fonction qui retourne l'arbre de huffman correspondant à partir du dictionnaire de fréquence dico"""
    arbres = sorted([AB(val, AB(cle)) for cle, val in dico.items()], key=lambda x: (x.get_val(), x.get_ag().get_val()))

    while len(arbres) > 1:
        ab1, ab2 = arbres.pop(0), arbres.pop(0)
        # print(ab1, ab2)
        arbres.append(AB(ab1.get_val() + ab2.get_val(), ab1, ab2))
        arbres = sorted(arbres, key=lambda x: x.get_val())

    return arbres[0]


def code_huffman(chaine, arbre):
    """Fonction qui retourne l'encodage binaire correspondant à la chaine à l'aide de l'arbre de huffman 'arbre'"""
    chaine_retour = ""
    ab1 = arbre
    for c in chaine:
        chemin_vers_car = find_path(arbre, c)[1:]
        for elem in chemin_vers_car:
            if elem == ab1.get_ag().get_val() and c in ab1.get_ag():
                chaine_retour += "1"
                ab1 = ab1.get_ag()
            else:
                chaine_retour += "0"
                ab1 = ab1.get_ad()
        ab1 = arbre

    return chaine_retour


def find_path(arbre, cible):
    """Fonction qui retourne le chemin vers une certaine feuille cible"""
    path = []

    def dfs(ab, cible):
        """Depth First Search qui permet de trouver le chemin"""
        if ab is None:
            return False
        path.append(ab.get_val())
        if ab.get_val() == cible:
            return True
        res = dfs(ab.get_ag(), cible)
        if res is True:
            return True
        res = dfs(ab.get_ad(), cible)
        if res is True:
            return True

        path.pop()
        return False

    dfs(arbre, cible)
    return path


# print(dechiffer("110110110000111100011001100111001000110100101010101111", AB_huffman1))
# print(frequence("EXEMPLE DE MESSAGE"))
# print(arbre_huffman(frequence("EXEMPLE DE MESSAGE")))
# print(code_huffman("EXEMPLE DE MESSAGE", arbre_huffman(frequence("EXEMPLE DE MESSAGE"))))

message = "EXEMPLE DE MESSAGE"
ab = arbre_huffman(frequence(message))
code_binaire = code_huffman(message, ab)
print(code_binaire)
print(dechiffer(code_binaire, ab))