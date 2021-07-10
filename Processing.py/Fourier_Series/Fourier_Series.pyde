from collections import deque

time = 0
wave = deque([], 350)

def setup():
    size(600, 400)
    frameRate(60)
    
def draw():
    global time
    
    background(51)
    translate(width/4, height/2)
    
    x, y = 0, 0
    
    for i in range(10):
        prevx = x
        prevy = y
        
        
        n = i * 2 + 1
        radius = 75 * (4 / (n * PI))  #
        x += radius * cos(n * time)   # square wave
        y += radius * sin(n * time)   #
        
        
        '''
        n = i + 1
        if n % 2:
            n = -n
        radius = 75 * (2 / (n * PI))  #
        x += radius * cos(n * time)   # sawtooth wave
        y += radius * sin(n * time)   #
        '''
    
        stroke(255, 100)
        noFill()
        ellipse(prevx, prevy, radius * 2, radius * 2)
        
        fill(255)
        line(prevx, prevy, x, y)
        #ellipse(x, y, 8, 8)
        
    wave.appendleft(y)
    transX = 150
    translate(transX, 0)
    line(x - transX, y, 0, wave[0])
    
    noFill()
    beginShape()
    for i in range(len(wave)):
        vertex(i, wave[i])
    endShape()
    
    
    time += 0.05
    
    
    
    
    
    
    
    
