class Vehicule:
    """Classe modélisant un vehicule"""

    # Constructeur
    def __init__(self, marque, vitesse):
        """Initialise les valeurs des attributs"""
        self.__marque = marque
        self.__vitesse = vitesse
        
    # Méthode est_une_voiture()
    def est_une_voiture(self):
        return False
        
    # Accesseurs
    def get_marque(self):
        return self.__marque
    
    def get_vitesse(self):
        return self.__vitesse
    
    # Méthode accelerer()
    def accelerer(self, dv):
        """Augmente la vitesse de dv"""
        self.__vitesse += dv
        
    # Méthode freiner()
    def freiner(self, dv):
        """Diminue la vitesse de dv"""
        self.__vitesse -= dv

class Voiture(Vehicule):
    """Classe qui hérite de Vehicule, modélisant une voiture"""
    
    # Constructeur
    def __init__(self, marque, vitesse, nb_portes):
        super().__init__(marque, vitesse)
        self.__nb_portes = nb_portes
    
    # Méthode est_une_voiture()
    def est_une_voiture(self):
        return True
    
class Moto(Vehicule):
    """Classe qui hérite de Vehicule, modélisant une moto"""
    
    # Constructeur
    def __init__(self, marque, vitesse, cylindree):
        super().__init__(marque, vitesse)
        self.__cylindree = cylindree
        
    
vehicule1 = Voiture('Peugeot',0,5)
vehicule1.accelerer(80)
print(vehicule1.get_marque(), ':', vehicule1.est_une_voiture(), '; vitesse :', vehicule1.get_vitesse(), 'km/h')
vehicule2 = Moto('Honda',0,750)
vehicule2.accelerer(120)
print(vehicule2.get_marque(), ':', vehicule2.est_une_voiture(), '; vitesse :', vehicule2.get_vitesse(), 'km/h')