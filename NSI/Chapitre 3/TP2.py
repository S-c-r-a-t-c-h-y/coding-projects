from pile import Pile       
        
        
def verifier(chaine):
    """Fonction qui vérifie si la chaine est bien parentésée
       Elle renvoie un booléen b qui vaut :
           - True si la chaine est bien parenthésée
           - False sinon
    """
    pile1 = Pile()
    for c in chaine :
        if c == '(':
            pile1.empiler('(')
        elif c == ')':
            if pile1.est_vide():
                return False
            pile1.depiler()
    return pile1.est_vide()


print('Entrer une expression parenthésée :')
expression = input()
print(verifier(expression))

    
        