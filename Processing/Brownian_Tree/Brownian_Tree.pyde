from particle import *

tree = []
current = None

def setup():
    global current
    size(600, 600)
    tree.append(Particle(3))
    tree[0].pos.set(width / 2, height / 2)
    tree[0].show()
    
    current = Particle(3)
    
    
def draw():
    global current
    background(51)
    
    while not current.intersects(tree):
        current.update()
        if not current.alive:
            current = Particle(3)
            
    tree.append(current)
    print(len(tree))
    
    current = Particle(3)
    
    for p in tree:
        p.show()
