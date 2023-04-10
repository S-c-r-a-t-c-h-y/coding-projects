from liste_chainee import *
           
def exemple():
    lc1 = Liste_chainee()
    
    for i in range(10):
        lc1.placer(i)
        
    print(lc1)
    return lc1

lc1 = exemple()
print(len(lc1))