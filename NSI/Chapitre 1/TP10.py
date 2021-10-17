class Personne:
    
    def __init__(self, nom, prenom):
        self.__nom = nom
        self.__prenom = prenom
        
    def get_nom(self):
        return self.__nom
    
    def get_prenom(self):
        return self.__prenom
    
    def presentation(self):
        pass
    
class Professeur(Personne):
    
    def __init__(self, nom, prenom, matiere):
        super().__init__(nom, prenom)
        self.__matiere = matiere
        
    def get_matiere(self):
        return self.__matiere
    
    def presentation(self):
        print(f"Bonjour je m'appelle {self.get_prenom()} {self.get_nom()} ; je suis professeur en {self.get_matiere()}")
    
class Eleve(Personne):
    
    def __init__(self, nom, prenom, classe):
        super().__init__(nom, prenom)
        self.__classe = classe
        
    def get_classe(self):
        return self.__classe
    
    def presentation(self):
        print(f"Bonjour je m'appelle {self.get_prenom()} {self.get_nom()} ; je suis élève en {self.get_classe()}")
    
    
prof1 = Professeur('Jean', 'Dupont', 'Mathématiques')
prof1.presentation()

eleve1 = Eleve('Jules', 'Morel', 'TA')
eleve1.presentation()



