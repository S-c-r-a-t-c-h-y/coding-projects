
class Turtle3D:
    
    def __init__(self, axiom, rules, step, angle, shrinking_coeff=0.85, line_color=255, transparency=0.3, bg_color=51):
        self.axiom = axiom
        self.rules = rules
        self.sentence = axiom
        
        self.step = step
        self.angle = radians(angle)
        self.shrinking_coeff = shrinking_coeff
        self.bg_color = bg_color

        if not(isinstance(line_color, (int, float))):
            r, g, b = line_color[:3]
            self.color = color(r, g, b, 255*transparency)
        else:
            self.color = color(line_color, 255*transparency)
        
        
    def generate_next(self):
        self.step *= self.shrinking_coeff
        new = ""
        for letter in self.sentence:
            new += self.rules.get(letter, letter) 
        self.sentence = new
        return self.sentence
    
    def generate_infinite(self):
        sentence = self.axiom
        while True:
            new = ""
            for letter in sentence:
                 new += self.rules.get(letter, letter) 
            sentence = new
            yield sentence
        
    def draw_shape(self):
        background(self.bg_color)
        resetMatrix()
        
        stroke(self.color)
        strokeWeight(1)
        noFill()
        
        line(0, 0, 0, -50)
        translate(width / 2, height / 2, 0)
        
        for car in self.sentence:
            if car == "F":
                line(0, 0, 0, -self.step)
                translate(0, -self.step, 0)
            elif car == "+":
                rotateZ(self.angle)
            elif car == "-":
                rotateZ(-self.angle)
            elif car == "&":
                rotateX(self.angle)
            elif car == "^":
                rotateX(-self.angle)
            elif car == "<":
                rotateY(self.angle)
            elif car == ">":
                rotateY(-self.angle)
                
            elif car == "[":
                pushMatrix()
            elif car == "]":
                popMatrix()
