class Ball:
    
    def __init__(self, x, y, size, speed, angle, color):
        self.x = x
        self.y = y
        self.size = size
        self.vector = PVector.fromAngle(radians(angle))
        for c in self.vector:
            c *= speed
        self.color = color
        
    def display(self):
        fill(self.color)
        stroke(self.color)
        circle(self.x, self.y, self.size)
        
    def move(self):
        self.x += self.vector.x
        self.y += self.vector.y
        
        if self.x < -self.size or self.x > width + self.size or self.y < -self.size or self.y > height + self.size:
            del self
            
    def update(self):
        self.move()
        self.display()
