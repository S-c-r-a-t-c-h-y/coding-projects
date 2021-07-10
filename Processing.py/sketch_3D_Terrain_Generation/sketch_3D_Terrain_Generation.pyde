
scl = 20
w = 1400
h = 2000

cols = w / scl
rows = h / scl

flying = 0
terrain = []

def setup():
    global terrain
    size(600, 600, P3D)
    terrain = [[0 for _ in range(rows)] for _ in range(cols)]


def draw():
    global flying, terrain
    background(0)
    
    flying -= 0.01
    yoff = flying
    for y in range(rows):
        xoff = 0
        for x in range(cols):
            terrain[x][y] = map(noise(xoff, yoff), 0, 1, -100, 100)
            xoff += 0.02
        yoff += 0.02
        
    fill(200, 50)
    translate(-w / 2, 0, -height / 4)
    rotateX(PI/3)
    translate(0, 50, 0)
    
    for y in range(rows-1):
        beginShape(TRIANGLE_STRIP)
        for x in range(cols):
            vertex(x * scl, y * scl, terrain[x][y])
            vertex(x * scl, (y + 1) * scl, terrain[x][y+1])
        endShape()
    
    
    
    
    
    
