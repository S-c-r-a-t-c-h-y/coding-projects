class Turtle2D:
    '''
    Extension of the L-System class that takes care of drawing the created fractals
    following specific rules
    '''
    
    def __init__(self, axiom, rules, step, angle, drawn_variables=["F"], shrinking_coeff=0.85, line_color=255, transparency=0.3, stroke_weight=1, bg_color=51, x=None, y=None):
        self.axiom = axiom
        self.rules = rules
        self.sentence = axiom
        self.drawn_variables = drawn_variables
        
        self.step = step
        self.angle = radians(angle)
        self.shrinking_coeff = shrinking_coeff
        self.bg_color = bg_color
        self.stroke_weight = stroke_weight

        if not(isinstance(line_color, (int, float))):
            r, g, b = line_color[:3]
            self.color = color(r, g, b, 255*transparency)
        else:
            self.color = color(line_color, 255*transparency)
            
        self.x = x
        self.y = y
        
        if self.x is None:
            self.x = width/2
        if self.y is None:
            self.y = height
        
        print(repr(self))
        
        
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
        strokeWeight(self.stroke_weight)
            
        translate(self.x, self.y)
        
        for car in self.sentence:
            if car in self.drawn_variables:
                line(0, 0, 0, -self.step)
                translate(0, -self.step)
            elif car == "+":
                rotate(self.angle)
            elif car == "-":
                rotate(-self.angle)
            elif car == "[":
                push()
            elif car == "]":
                pop()
                
    def __repr__(self):
        return 'Turle2D(axiom={}, rules={},\nstep={}, angle={}, drawn_variables={}, shrinking_coeff={},\nstroke_weight={}, bg_color={}, x={}, y={}, color={})\n'.format(self.axiom, self.rules, self.step, degrees(self.angle), self.drawn_variables, self.shrinking_coeff, self.stroke_weight, self.bg_color, self.x, self.y, self.color)
        
        
        
        
        
        
