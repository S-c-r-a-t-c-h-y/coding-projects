class Complex:
    
    def __init__(self, a, b):
        self.re = a
        self.im = b
        
        
    def __mul__(self, c):
        re = self.re * c.re - self.im * c.im
        im = self.re * c.im + self.im * c.re
        return Complex(re, im)
    
    
    def __add__(self, c):
        re = self.re + c.re
        im = self.im + c.im
        return Complex(re, im)


def dft(x):
    X = []
    N = len(x)
    
    for k in range(N):
        sum = Complex(0, 0)
        for n in range(N):
            phi = (TWO_PI * k * n) / N
            c = Complex(cos(phi), -sin(phi))
            sum += x[n] * c
        
        sum.re /= N
        sum.im /= N
        
        freq = k
        amp = sqrt(sum.re ** 2 + sum.im ** 2)
        phase = atan2(sum.im, sum.re)
        
        X.append({'re': sum.re, 'im': sum.im, 'freq': freq, 'amp': amp, 'phase': phase})
        
    return X
