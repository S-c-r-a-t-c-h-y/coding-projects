from arbre_binaire import AB
from dessiner_arbre import dessiner

arbre1 = AB(5, AB(4, AB(2), AB(3)), AB(8, AB(9), AB(1)))

print(arbre1)
dessiner(arbre1)
