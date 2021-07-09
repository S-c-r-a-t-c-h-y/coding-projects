class LSystem:
    '''
    Basic L-System with no drawing abilities
    '''
    
    def __init__(self, axiom, rules):
        self.axiom = axiom
        self.rules = rules
        self.sentence = axiom
        
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
