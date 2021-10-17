from liste_chainee import *
           
def exemple():
    lc1 = Liste_chainee()
    for i in range(6):
        lc1.placer(i)
    return lc1

lc1 = exemple()
lc1.placer_fin(8)
print(lc1)

print(3 in lc1)
print(7 in lc1)
