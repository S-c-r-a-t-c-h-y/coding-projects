class Arbre:
    """Classe modélisant un arbre"""
    
    compteur = 0
    
    # Constructeur
    def __init__(self, espece, age, taille, croissance_annuelle):
        """Initialise les valeurs des attributs"""
        self.__espece = espece
        self.__age = age
        self.__taille = taille
        self.__croissance_annuelle = croissance_annuelle
        Arbre.compteur += 1
        
    # Méthode afficher() 
    def afficher(self):
        print('Espèce :', self.__espece)
        print('Age :', self.__age, 'ans')
        print(f'Taille : {self.__taille} mètres')
        print(f'Croissance annuelle : {self.__croissance_annuelle} mètres par an')
        
    # Méthode grandir()
    def grandir(self, nb):
        """Méthode qui fait grandir l'arbre de nb années"""
        self.__age += nb
        self.__taille += self.__croissance_annuelle * nb

arbre1 = Arbre("sapin", 5, 3, 0.5)
arbre2 = Arbre("chêne", 10, 2, 0.2)
arbre3 = Arbre("saule", 8, 4, 0.5)
arbre4 = Arbre("bouleau", 12, 4, 0.3)

arbre1.__espece = 'pin'
arbre1.afficher()
    