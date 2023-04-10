
points = []
outter = None

def setup():
    global outter
    size(600, 600)
    for _ in range(20):
        points.append(PVector(random(50, width - 50), random(50, height - 50)))
    points.sort(key=lambda x: x.x)
    
    outter = JarvisMarch(points)
    print(outter)
    
    
    

def draw():
    background(51)
    stroke(255)
    strokeWeight(4)
    
    for p in points:
        point(p.x, p.y)
        
    fill(255, 50)
    beginShape()
    for p in outter:
        vertex(p.x, p.y)
    endShape(CLOSE)
        
        
def JarvisMarch(E):
    current = E[1]
    hull = [E[0]]
    while current != None:
        hull.append(current)
        
        max_a = -10000
        max_p = None
        for checking in E:
            if checking not in hull:
                try:
                    a = (checking.x - current.x) / (checking.y - current.y)
                    if a >= max_a:
                        max_a = a
                        max_p = checking
                except:
                    pass
        current = max_p
    return hull
    
        
        
'''
max_a = -10000
        max_p = None
        for p2 in points:
            try:
                a = (p2.x - p.x) / (p2.y - p.y)
                if a >= max_a:
                    max_a = a
                    max_p = p2
            except:
                pass
        p = max_p
'''    
        
        
        
        
        
