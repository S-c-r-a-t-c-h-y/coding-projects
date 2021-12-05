from arbre_binaire import AB
from dessiner_arbre import dessiner


class ABR(AB):
    """Structure abstraite de données d'arbre binaire de recherche"""

    # Constructeur
    def __init__(self, val):
        super().__init__(val)

    def inserer(self, val):
        """Méthode pour insérer une nouvelle valeur dans l'arbre"""

        if val < self.get_val():
            if self.get_ag() is None:
                self.set_ag(ABR(val))
            else:
                self.get_ag().inserer(val)
        else:
            if self.get_ad() is None:
                self.set_ad(ABR(val))
            else:
                self.get_ad().inserer(val)

    def copy(self):
        """Retourne une copie de l'arbre"""

        new_abr = ABR(self.get_val())
        new_abr.set_ad(self.get_ad())
        new_abr.set_ag(self.get_ag())
        return new_abr


if __name__ == "__main__":
    abr1 = ABR(6)
    abr1.inserer(4)
    abr1.inserer(8)
    abr1.inserer(2)
    abr1.inserer(5)
    abr1.inserer(9)
    abr1.inserer(7)

    dessiner(abr1)
