from dico1 import entrer_dico
import tkinter as tk
import time
import win32gui

def inverser_dico(dico):
    return {valeur: cle for cle, valeur in dico.items()}

class Morse(tk.Tk):
    
    dico_morse = entrer_dico('morse.csv', str)
    
    def __init__(self, texte):
        tk.Tk.__init__(self)
        self.geometry("400x400")
        self.title("Morse")
        
        self.texte = texte
        
        self.canvas = tk.Canvas(self, width=400, height=400, bg='black')
        self.canvas.pack()
        self.cercle = self.canvas.create_oval(150, 150, 250, 250, fill='black')
        
        self.impulsions = {'.': 1, '-': 3, ' ': 3, '/': 7}
        self.duree_impulsion = 100
        
        self.focus_force()
        self.animer()
        
        self.mainloop()
    
    def animer(self):
        for car in self.texte:
            nb = self.impulsions[car]
            if car in '.-':
                self.canvas.itemconfigure(self.cercle, fill='yellow')
            self.update()
            self.canvas.after(self.duree_impulsion*nb)
            self.canvas.itemconfigure(self.cercle, fill='black')
            self.update()
            self.canvas.after(self.duree_impulsion)
            
        self.destroy()
    
    @staticmethod
    def dechiffrer(morse):
        dico = inverser_dico(Morse.dico_morse)
        return ''.join(dico.get(symbol, '') for symbol in morse.split(' '))
    
    @staticmethod
    def morse(phrase):
        phrase = phrase.upper()
        rep = ''
        for lettre in phrase:
            rep += Morse.dico_morse[lettre]
            rep += ' '
        return rep
        
texte = str(input("Saisir un texte : ")).upper()
texte_encripte = Morse.morse(texte)
decripteur = Morse(texte_encripte)