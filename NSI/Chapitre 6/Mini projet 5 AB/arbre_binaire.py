class AB:
    """Structure abstraite de données d'arbre binaire"""

    # Constructeur
    def __init__(self, val, ag=None, ad=None):
        self.__val = val  # étiquette du noeud
        self.__ag = ag  # sous-arbre gauche
        self.__ad = ad  # sous-arbre droit

    # Accesseurs
    def get_val(self):
        return self.__val

    def get_ag(self):
        return self.__ag

    def get_ad(self):
        return self.__ad

    # Mutateurs
    def set_val(self, val):
        self.__val = val

    def set_ag(self, arbre):
        self.__ag = arbre

    def set_ad(self, arbre):
        self.__ad = arbre

    def hauteur_tout_a_droite(self):
        """Retourne la hauteur entre la racine et la feuille de l'arbre située la plus à droite"""

        if self.__ad is None:
            return 1
        hd = self.__ad.hauteur_tout_a_droite()
        return hd + 1

    def hauteur(self):
        """Retourne la hauteur de l'arbre"""

        if self.__ag is None and self.__ad is None:
            return 1
        if self.__ag is None:
            hd = self.__ad.hauteur()
            return hd + 1
        if self.__ad is None:
            hg = self.__ag.hauteur()
            return hg + 1
        hg = self.__ag.hauteur()
        hd = self.__ad.hauteur()
        return max(hg, hd) + 1

    def taille(self):
        """Retourne la taille de l'arbre"""

        if self.__ag is None and self.__ad is None:
            return 1
        if self.__ag is None:
            hd = self.__ad.taille()
            return hd + 1
        if self.__ad is None:
            hg = self.__ag.taille()
            return hg + 1
        hg = self.__ag.taille()
        hd = self.__ad.taille()
        return hg + hd + 1

    def copy(self):
        """Retourne une copie de l'arbre"""
        new_ab = AB(self.__val)
        new_ab.set_ad(self.__ad)
        new_ab.set_ag(self.__ag)
        return new_ab

    def __repr__(self):
        """Surcharge de la fonction print()"""

        def AB_tuple(arbre):
            if arbre != None:
                return (arbre.get_val(), AB_tuple(arbre.get_ag()), AB_tuple(arbre.get_ad()))

        return str(AB_tuple(self))

    def __contains__(self, valeur):
        """Surcharge de l'opérateur d'appartenance"""

        if self.__val == valeur:
            return True
        if self.__ag is None and self.__ad is None:
            return False
        if self.__ag is None:
            return valeur in self.__ad
        if self.__ad is None:
            return valeur in self.__ag
        return any((valeur in self.__ad, valeur in self.__ag))


if __name__ == "__main__":
    # arbre1 = AB(12, AB(10, AB(7)), AB(20, AB(15), AB(25)))
    # arbre2 = AB(12, AB(10, AB(7)))
    # arbre3 = AB(12, AB(10, AB(7), AB(11)), AB(20))

    # print(arbre1.hauteur_tout_a_droite())
    # print(arbre2.hauteur_tout_a_droite())
    # print(arbre3.hauteur_tout_a_droite())

    # arbre1 = AB(2)
    # arbre2 = AB(5, AB(6), AB(2))
    # arbre3 = AB(1, AB(2, AB(4, AB(5), AB(6))))

    # print(arbre1.hauteur())
    # print(arbre2.hauteur())
    # print(arbre3.hauteur())

    # print(arbre1.taille())
    # print(arbre2.taille())
    # print(arbre3.taille())

    # print(1 in arbre3)
    # print(2 in arbre3)
    # print(8 in arbre3)

    pass
