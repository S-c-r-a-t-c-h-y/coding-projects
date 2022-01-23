from square import *

class Ball:
    
    balls = []

    def __init__(self, x, y, radius, mass=1, initial_velocity=PVector(0, 0), movable=True, color="#000000", maxspeed=50, debug=False):
        self.pos = PVector(x, y)
        self.radius = radius
        self.vel = initial_velocity
        self.acc = PVector(0, 0)
        self.mass = mass
        self.color = color
        self.maxspeed = maxspeed
        self.movable = movable
        
        self.debug = createGraphics(width, height)
        self.do_debug = debug
        
        Ball.balls.append(self)

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
        circle(self.pos.x, self.pos.y, self.radius*2)
        
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
                distance_vect = PVector.sub(self.pos, ball.pos)
                min_distance = self.radius + ball.radius
                if distance_vect.mag() < min_distance:
                    # corrects the position of the ball before proceeding to collide
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
                    
                    if ball.movable:
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
                    else:
                        dir.mult(self.vel.mag())
                        
                        
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
                    
        for rectangle in Rectangle.rectangles:
            w = rectangle.width
            h = rectangle.height
            
            half_width = w / 2
            half_height = h / 2
            
            center = PVector(rectangle.pos.x + half_width, rectangle.pos.y + half_height)
            vect_distance = PVector.sub(self.pos, center)
            
            x = constrain(vect_distance.x, -half_width, half_width)
            y = constrain(vect_distance.y, -half_height, half_height)
            
            clamped = PVector(x, y, 0)
            closest = PVector.add(center, clamped)
            
            distance_vector = PVector.sub(self.pos, closest)
            d = distance_vector.mag()
            
            #print(d)

            stroke(255, 0, 0)
            strokeWeight(20)
            print(closest.x, closest.y)
                                    
            if d < self.radius: # collision
                points = [rectangle.pos.copy(), PVector(rectangle.pos.x + w, rectangle.pos.y), PVector(rectangle.pos.x + w, rectangle.pos.y + h), PVector(rectangle.pos.x, rectangle.pos.y + h), rectangle.pos.copy()]
                
                for i in range(0, 4):
                    x1, y1 = points[i].x, points[i].y
                    x2, y2 = points[i+1].x, points[i+1].y
                    
                    try:
                        a1 = (y2-y1)/(x2-x1)
                        b1 = y1 - a1 * x1
                        # y = ax + b
                        
                        on_line = closest.y == a1 * closest.x + b1
                    except ZeroDivisionError:
                        on_line = closest.x == x1
                        
                    if on_line:
                        
                        """
                        vect_distance = PVector.sub(self.pos, center).mult(1000)
                        x = constrain(vect_distance.x, -half_width, half_width)
                        y = constrain(vect_distance.y, -half_height, half_height)
            
                        dist_to_border = PVector(x, y, 0).mag()
                        
                        self.pos.set(center)
                        correction_vector = distance_vector.copy()
                        correction_vector.setMag(dist_to_border + self.radius)
                        self.pos.add(correction_vector)
                        """
                        
                        correction_vector = PVector.mult(self.vel, -1)
                        self.pos.add(correction_vector)
                        
                        
                        # calculates the vector normal of the collision and normalizes it
                        surface_vector = PVector.sub(points[i+1], points[i])
                        normal = surface_vector.copy()
                        normal.rotate(HALF_PI)
                        normal.normalize()
                        
                        # calculates the incidence vector of the collision and normalizes it
                        incidence = PVector.mult(self.vel, -1)
                        incidence.normalize()
                        
                        # dot product of the incidence vector with the normal vector
                        dot = incidence.dot(normal)
                        
                        # calculates the new trajectory (dir vector) based on the equation R = 2N(N.L)-L where R is the reflection vector, N is the normal, and L is the incident vector.
                        dir = PVector(2 * normal.x * dot - incidence.x, 2 * normal.y * dot - incidence.y, 0)
                        dir.normalize()
                        dir.mult(self.vel.mag())
                        
                        self.vel = dir
                        
                        break
                

"""
normal = PVector(1, 0)
incidence = PVector.mult(self.vel, -1)
            
dot = incidence.dot(normal)
self.vel.set(2*normal.x*dot - incidence.x, 2*normal.y*dot - incidence.y, 0)
"""
