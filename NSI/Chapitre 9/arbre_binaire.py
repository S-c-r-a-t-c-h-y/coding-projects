class AB:
    """Structure abstraite de données d'arbre binaire"""

    # Constructeur
    def __init__(self, val=None, ag=None, ad=None):
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

    def __repr__(self):
        """Surcharge de la fonction print()"""

        def AB_tuple(arbre):
            if arbre != None:
                return (arbre.get_val(), AB_tuple(arbre.get_ag()), AB_tuple(arbre.get_ad()))

        return str(AB_tuple(self))

    def hauteur_tout_a_droite(self):
        if self.__ad == None:
            return 1
        else:
            hd = self.__ad.hauteur_tout_a_droite()
            return 1 + hd

    def hauteur(self):
        # Cas d'une feuille
        if self.__ag == None and self.__ad == None:
            return 1
        # Cas où il n'y a pas de fils gauche, mais un fils droit
        elif self.__ag == None:
            return 1 + self.__ad.hauteur()
        # Cas où il n'y a pas de fils droit, mais un fils gauche
        elif self.__ad == None:
            return 1 + self.__ag.hauteur()
        # Cas où il y a un fils gauche et un fils droit
        else:
            hg = self.__ag.hauteur()
            hd = self.__ad.hauteur()
            return max(hg, hd) + 1

    def taille(self):
        if self.__ag == None and self.__ad == None:
            return 1
        elif self.__ag == None:
            return 1 + self.__ad.taille()
        elif self.__ad == None:
            return 1 + self.__ag.taille()
        else:
            tg = self.__ag.taille()
            td = self.__ad.taille()
            return tg + td + 1

    def __contains__(self, val):
        if self.__val == val:
            return True
        elif self.__ag == None and self.__ad == None:
            return False
        elif self.__ad == None:
            return val in self.__ag
        elif self.__ag == None:
            return val in self.__ag
        else:
            return val in self.__ag or val in self.__ad
