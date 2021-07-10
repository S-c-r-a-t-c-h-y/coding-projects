from balls import Ball

i = 0
balls = []
nb_rays = 8

def setup():
    size(200, 200)
    colorMode(HSB, 360, 100, 100)
    
def draw():
    global i
    
    if frameCount % 3:
        background(51)
        # strokeWeight(5)
        
        for k in range(1, nb_rays + 1):
            temp = i + (360 / nb_rays) * k
            if temp > 360:
                temp -= 360
                
            b = Ball(width/2, height/2, 10, 4, temp, color(i, 100, 100))
            balls.append(b)
            
        for ball in balls:
            ball.update()
            
        i += 1
        if i > 360:
            i -= 360
    
