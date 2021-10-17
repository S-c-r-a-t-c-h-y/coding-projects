from pile import Pile

        
def exemple():
    """ Fonction faisant évoluer une pile nommée pile1"""
    pile1 = Pile()
    pile1.empiler(5)
    pile1.empiler(1)
    pile1.depiler()
    pile1.empiler(2)
    pile1.empiler(7)
    pile1.empiler(3)
    pile1.depiler()
    pile1.afficher()
    
exemple()