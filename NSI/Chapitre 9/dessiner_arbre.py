from binarytree import Node, tree
# exemple d'utilisation de binarytree :
# arbre = Node(1,Node(2),Node(3,Node(4),Node(5)))
# print(arbre)

def dessiner(arbre):
    # Exemple
    # Transforme "(1,None,None)" en "Node(1,None,None)" compris par la bibliotheque
    # binarytree
    commande = str(arbre).replace("(","Node(")
    
    # Exemple
    # execute la commande arbre_bt=Node(1,None,None)
    # puis la commande print(arbre_bt)
    # avec le print surchargé de la bibliotheque binarytree
    exec("arbre_bt = " + commande + "\n" + "print(arbre_bt)")