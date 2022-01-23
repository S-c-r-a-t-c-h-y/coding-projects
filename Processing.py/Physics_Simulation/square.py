class Rectangle:
    
    rectangles = []

    def __init__(self, x, y, w, h, mass=1, initial_velocity=PVector(0, 0), movable=True, color="#000000", maxspeed=50, debug=False):
        self.pos = PVector(x, y)
        self.width = w
        self.height = h
        
        self.vel = initial_velocity
        self.acc = PVector(0, 0)
        
        self.mass = mass
        self.maxspeed = maxspeed
        self.movable = movable
        
        self.color = color
        
        self.debug = createGraphics(width, height)
        self.do_debug = debug
        
        Rectangle.rectangles.append(self)

    def update(self):
        if self.movable:
            self.edges()
            self.detect_collisions()
            
            self.vel.add(self.acc)
            self.vel.limit(self.maxspeed)
            self.pos.add(self.vel)
        
            self.acc.mult(0)

    def display(self):
        if self.do_debug and not self.movable:
            strokeWeight(2)
            stroke(0, 0, 255)
        else:
            strokeWeight(1)
            stroke(0)
            
        fill(map(self.mass, 1, 50, 225, 0))
        rectMode(CORNER)
        rect(self.pos.x, self.pos.y, self.width, self.height)
        
        # --------------- DEBUG --------------- #
        if self.do_debug:
            self.debug.beginDraw()
            self.debug.endDraw()
            
            image(self.debug, 0, 0)
        # ------------------------------------- #

    def apply_force(self, force):
        self.acc.add(force)

    def edges(self):
        if self.pos.x + self.radius > width:
            self.pos.x = width - self.radius
            self.vel.x *= -1
            
        if self.pos.x - self.radius < 1:
            self.pos.x = self.radius
            self.vel.x *= -1
            
        if self.pos.y + self.radius > height:
            self.pos.y = height - self.radius
            self.vel.y *= -1
            
        if self.pos.y - self.radius < 1:
            self.pos.y = self.radius
            self.vel.y *= -1
                
    def detect_collisions(self):
        for ball in Ball.balls:
            if ball is not self:
                d = PVector.dist(self.pos, ball.pos)
                if d < (self.radius + ball.radius):
                    self.collide_with_ball(ball)
            
    def collide_with_ball(self, ball):
        
        
        distance_vect = PVector.sub(self.pos, ball.pos)
        min_distance = self.radius + ball.radius
        
        self.pos.set(ball.pos)
        correction_vector = distance_vect.copy()
        correction_vector.setMag(min_distance)
        
        self.pos.add(correction_vector)
        
        
        # calculates the vector normal of the collision and normalizes it
        normal = PVector.sub(self.pos, ball.pos)
        normal.normalize()
        
        # calculates the incidence vector of the collision and normalizes it
        incidence = PVector.mult(self.vel, -1)
        incidence.normalize()
        
        # dot product of the incidence vector with the normal vector
        dot = incidence.dot(normal)
        
        # calculates the new trajectory (dir vector) based on the equation R = 2N(N.L)-L where R is the reflection vector, N is the normal, and L is the incident vector.
        dir = PVector(2 * normal.x * dot - incidence.x, 2 * normal.y * dot - incidence.y, 0)
        dir.normalize()
        
        # calculates the new velocity using the elastic motion fomula
        # (conservation of momentum and kinetic enery)
        # https://www.toppr.com/guides/physics-formulas/elastic-formula/#:~:text=An%20elastic%20collision%20is%20a,2%20(v2f)2.
        m1 = self.mass
        m2 = ball.mass
        v1 = self.vel.mag()
        v2 = ball.vel.mag()
        
        ke = 1/2 * m1 * v1 ** 2 + 1/2 * m2 * v2 ** 2
        p = m1 * v1 + m2 * v2
        
        a = m2 ** 2
        b = -2 * ke * m2 + m1 * m2
        c = -1 * (2 * m1 * p - ke ** 2)
        
        v2f = (-1 * b - (b**2 - 4*a*c) ** 0.5)/(2*a)
        v1f = (ke - m2*v2f)/m1
        
        # v2f = (-1 * b + (b**2 - 4*a*c) ** 0.5)/(2*a)
        # v1f = (ke - m2*v2f)/m1
        
        # applies the newly calculated velocity to the new trajectory
        dir.mult(v1f)
        
        # --------------- DEBUG --------------- #
        amplitude = 20
        
        self.debug.beginDraw()
        
        self.debug.clear()
        
        self.debug.stroke(255, 0, 0)
        self.debug.line(self.pos.x, self.pos.y, self.pos.x + self.vel.x * amplitude, self.pos.y + self.vel.y * amplitude)
        
        self.debug.stroke(0, 255, 0)
        self.debug.line(self.pos.x, self.pos.y, self.pos.x + dir.x * amplitude, self.pos.y + dir.y * amplitude)
        
        self.debug.endDraw()
        # ------------------------------------- #
        
        # applies the new vector velocity
        self.vel = dir

# https://learnopengl.com/In-Practice/2D-Game/Collisions/Collision-detection
