class Arbre:
    """Classe modélisant un arbre"""
    
    compteur = 0
    
    # Constructeur
    def __init__(self, espece, age, taille, croissance_annuelle):
        """Initialise les valeurs des attributs"""
        self.espece = espece
        self.age = age
        self.taille = taille
        self.croissance_annuelle = croissance_annuelle
        Arbre.compteur += 1
        
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

arbre1 = Arbre("sapin", 5, 3, 0.5)
arbre2 = Arbre("chêne", 10, 2, 0.2)
arbre3 = Arbre("saule", 8, 4, 0.5)
arbre4 = Arbre("bouleau", 12, 4, 0.3)

print(f"Le nombre d'instance de la classe Arbre est {Arbre.compteur} .")
    