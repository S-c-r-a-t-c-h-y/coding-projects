from arbre_binaire import AB


class ABR(AB):
    """Structure abstraite de données d'arbre binaire de recherche"""

    # Constructeur
    def __init__(self, val):
        super().__init__(val)

    # Méthode pour insérer une nouvelle valeur
    def inserer(self, val):
        if val < self.get_val():
            if self.get_ag() == None:
                self.set_ag(ABR(val))
            else:
                self.get_ag().inserer(val)
        else:
            if self.get_ad() == None:
                self.set_ad(ABR(val))
            else:
                self.get_ad().inserer(val)
