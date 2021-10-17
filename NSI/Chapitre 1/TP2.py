class Arbre:
    """Classe modélisant un arbre"""
    
    # Constructeur
    def __init__(self, espece, age, taille, croissance_annuelle):
        """Initialise les valeurs des attributs"""
        self.espece = espece
        self.age = age
        self.taille = taille
        self.croissance_annuelle = croissance_annuelle
        
    # Méthode afficher() 
    def afficher(self):
        print('Espèce :', self.espece)
        print('Age :', self.age, 'ans')
        print(f'Taille : {self.taille} mètres')
        print(f'Croissance annuelle : {self.croissance_annuelle} mètres par an')
        
    # Méthode grandir()
    def grandir(self, nb):
        """Méthode qui fait grandir l'arbre de nb années"""
        self.age += nb
        self.taille += self.croissance_annuelle * nb
        
arbre1 = Arbre('sapin', 5, 3, 0.5)
arbre1.afficher()
print()
arbre1.grandir(2)
arbre1.afficher()
    