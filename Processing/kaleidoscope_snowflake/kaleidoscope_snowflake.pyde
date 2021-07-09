
symmetry = 6
angle = 360 / symmetry
x_off = 0

def setup():
    size(600, 600)
    background(51)
    colorMode(HSB, 360, 100, 100, 100)
    
def draw():
    global x_off
    translate(width/2, height/2)
    
    if mouseX > 0 and mouseX < width and mouseY > 0 and mouseY < height:
        
        mx = mouseX - width / 2
        my = mouseY - height / 2
        pmx = pmouseX - width / 2
        pmy = pmouseY - height / 2
        
        if mousePressed:
            c = map(sin(x_off), -1, 1, 0, 360)
            x_off += 0.05
            stroke(c, 100, 100, 40)
            strokeWeight(5)
            
            for i in range(symmetry):
                rotate(radians(angle))
                line(mx, my, pmx, pmy)
                push()
                scale(1, -1)
                line(mx, my, pmx, pmy)
                pop()

    if keyPressed:
        if key == 'd':
            background(51)
                
                
                
                
