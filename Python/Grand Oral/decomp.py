import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from math import pi, sin

def integrale(f, a, b, n=50):
    somme = 0
    h = float(b-a) / n
    x = a
    for _ in range(0, n + 1):
        somme += f(x) * h
        x += h
    return somme

def calculer_coeff(f, n=5):
    coeffs = []
    for i in range(n):
        y = lambda x: f(x) * sin((i+1)*pi*x)
        coeffs.append(2 * integrale(y, 0, 1))
    return coeffs

def approx_f(f, n=50):
    coeffs = calculer_coeff(f, n)
    return lambda x: sum(coeffs[i] * sin((i+1) * pi * x) for i in range(n))


f = lambda x: x ** 2
f = lambda x: 0.5 - abs(x - 0.5)
new_f = approx_f(f, 50)

fig = plt.figure(figsize=(10, 6))
plt.plot([f(i/100) for i in range(100)])
plt.plot([new_f(i/100) for i in range(100)])
plt.show()

print()