from arbre_binaire import AB
from dessiner_arbre import dessiner


def parfait(ngd):
    """
    Fonction qui renvoit un arbre binaire parfait à partir de
    son parcourt en profondeur préfixe ngd de type str
    """
    cle = ngd[0]
    ab1 = AB(cle)
    if len(ngd) > 1:
        ngd_g = ngd[1 : len(ngd) // 2 + 1]
        ngd_d = ngd[len(ngd) // 2 + 1 :]
        # print(ngd, ngd_g, ngd_d, sep="/")
        ab1.set_ag(parfait(ngd_g))
        ab1.set_ad(parfait(ngd_d))
    return ab1


def dechiffrer(chaine_morse):
    """Fonction qui déchiffre une chaine de caractère morse à l'aide d'un arbre binaire"""
    retour = ""

    # arbre binaire pour les codes morse
    ab = parfait(" EISHVUF ARL WPJTNDBXKCYMGZQO  ")

    # arbre binaire servant au parcours
    ab1 = ab

    for car in chaine_morse:
        if car == ".":
            ab1 = ab1.get_ag()
        elif car == "-":
            ab1 = ab1.get_ad()
        elif car == " ":
            retour += ab1.get_val()
            ab1 = ab  # réinitialise le parcours
        else:
            retour += ab1.get_val()
            retour += " "
            ab1 = ab

    retour += ab1.get_val()
    return retour


assert dechiffrer("-... --- -. -. ./.--- --- ..- .-. -. . .") == "BONNE JOURNEE"
assert dechiffrer("-... --- -. .--- --- ..- .-./-- --- -. ... .. . ..- .-.") == "BONJOUR MONSIEUR"
print("Tous les tests sont satisfaits")
