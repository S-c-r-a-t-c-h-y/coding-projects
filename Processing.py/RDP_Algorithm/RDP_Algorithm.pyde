
allPoints = []
epsilon = 0 

def setup():
    global rdp
    size(400, 400)
    
    for x in range(width):
        xval = map(x, 0, width, 0, 5);
        yval = exp(-xval) * cos(TWO_PI*xval);
        y = map(yval, -1, 1, height, 0);
        allPoints.append(PVector(x, y));

def draw():
    global epsilon
    
    background(51)
    stroke(255)
    noFill()
    
    beginShape()
    for v in allPoints:
        vertex(v.x, v.y)
    endShape()
        
    stroke(255, 0, 0)
    
    rdp = RDP(allPoints, epsilon)
    print(epsilon)
    epsilon += 1
    if epsilon > 100:
        epsilon = 0
    
    beginShape();
    for v in rdp:
        vertex(v.x, v.y)
    endShape();
    
    
    
    
def RDP(points, seuil):
    dmax = 0
    index = -1
    for i in range(1, len(points)-1):
        seg = PVector(points[-1].x - points[0].x, points[-1].y - points[0].y)
        m = seg.x / seg.y
        x = points[-1].x
        y = points[-1].y
        b = y - m * x
        d = abs(m * points[i].x - points[i].y + b)/sqrt(m**2+1)
        
        if d > dmax:
            index = i
            dmax = d
                 
    if dmax > seuil:
        recPoints1 = RDP(points[:index+1], seuil)
        recPoints2 = RDP(points[index:], seuil)
        
        return recPoints1[:-1] + recPoints2

    else:
        return [points[0], points[-1]]
