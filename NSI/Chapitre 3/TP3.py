from pile import Pile 

        
def palindrome(chaine):
    """Fonction qui vérifie si la chaine est un palindrome
       Elle renvoie un booléen b qui vaut :
           - True si la chaine est un palindrome
           - False sinon
    """
    pile1 = Pile()
    l = len(chaine)
    chaine1, chaine2 = chaine[:l//2], chaine[l//2+1:] if l % 2 else chaine[l//2:]
    for c in chaine1 :
        pile1.empiler(c)
        
    for c in chaine2 :
        if c != pile1.depiler():
            return False
    return True


print('Entrer une expression :')
expression = input()
print(palindrome(expression))