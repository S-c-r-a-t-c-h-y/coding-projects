class Menu:
    """Classe modélisant un menu"""
    
    # Constructeur
    def __init__(self, entree, plat, dessert, prix):
        """Initialise les valeurs des attributs"""
        self.entree = entree
        self.plat = plat
        self.dessert = dessert
        self.prix = prix
        
    # Méthode afficher() 
    def afficher_menu(self):
        print('Menu à', self.prix, 'euros :')
        print()
        print('Entrée :', self.entree)
        print('Plat :', self.plat)
        print('Dessert :', self.dessert)
        
            
menu1 = Menu('salade verte', 'gratin dauphinois', 'gâteau au chocolat', 29)
menu1.afficher_menu()
    