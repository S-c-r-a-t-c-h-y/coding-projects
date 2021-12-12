from arbre_binaire import AB

AB_huffman1 = AB(
    "",
    AB("", AB("E"), AB("", AB("", AB("G"), AB("A")), AB("", AB("D"), AB("L")))),
    AB("", AB("", AB("", AB("P"), AB("X")), AB("S")), AB("", AB(" "), AB("M"))),
)


def dechiffer(chaine_binaire):
    """Fonction qui permet de déchiffrer une chaine binaire en
    utilisant un arbre de Huffman."""

    chaine_retour = ""
    ab1 = AB_huffman1
    for c in chaine_binaire:
        if c == "1":
            ab1 = ab1.get_ag()
            if ab1.get_ad() is None and ab1.get_ag() is None:
                chaine_retour += ab1.get_val()
                ab1 = AB_huffman1
