class Compte:
    # classe modélisant un compte bancaire
    
    def __init__(self, numero, solde):
        self.numero = numero
        self.solde = solde
        
    # affiche le solde du compte
    def afficher_solde(self):
        print(f'Le solde du compte numéro {self.numero} est de {self.solde}.')
    
    # fait un crédit à la banque
    def credit(self, somme):
        self.solde += somme
        
    # débite une certaine somme du solde
    def debit(self, somme):
        self.solde -= somme
    
    
compte1 = Compte(274569183746, 517.27)
compte1.afficher_solde()
compte1.credit(1000.0)
compte1.afficher_solde()
compte1.debit(500.0)
compte1.afficher_solde()
