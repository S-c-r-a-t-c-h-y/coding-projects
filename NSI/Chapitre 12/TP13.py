from PIL import Image, ImageTk
import tkinter as tk
import time


class App(tk.Tk):
    def __init__(self, image_path):
        tk.Tk.__init__(self)

        self.image_originale = Image.open(image_path)
        self.image = Image.open(image_path)
        self.image_to_tk(self.image)
        self.img_w, self.img_h = self.image.size

        self.title("Rotation d'image")
        self.geometry(f"{self.img_w}x{self.img_h}")
        self.resizable(width=False, height=False)

        self.lbl = tk.Label(self, image=self.image_tk)
        self.lbl.pack()

        self.img_cnt = 0
        self.run()
        self.mainloop()

    def image_to_tk(self, image):
        self.image_tk = ImageTk.PhotoImage(image)
        return self.image_tk

    def run(self):
        self.rotation(self.image)
        self.show()

    def show(self, image=None, x=0, y=0):
        if image is None:
            image = self.image_originale

        img = self.image_originale
        img.paste(image, (x, y))
        img_name = f'GIF/IMG_{str(self.img_cnt).rjust(4, "0")}.png'

        # img.save(img_name, "PNG")

        self.img_cnt += 1

        self.image_to_tk(img)
        self.lbl.configure(image=self.image_tk)
        self.update()

    def rotation(self, image, x=0, y=0):
        m, n = image.size
        # dimensions de l’image
        assert m == n, "l’image doit être carrée"
        assert n & (n - 1) == 0, "la dimension doit être une puissance de 2"
        # Pas de cas de base : si n = 1 on ne fait rien
        if n > 1:
            k = n // 2
            # Diviser : découpe des blocs
            a = image.crop((0, 0, k, k))
            b = image.crop((k, 0, n, k))
            c = image.crop((k, k, n, n))
            d = image.crop((0, k, k, n))
            # Résoudre : rotation des blocs
            a = self.rotation(a, x, y)
            b = self.rotation(b, x + k, y)
            c = self.rotation(c, x + k, y + k)
            d = self.rotation(d, x, y + k)
            # Combiner : permutation des blocs
            image.paste(a, (k, 0))
            image.paste(b, (k, k))
            image.paste(c, (0, k))
            image.paste(d, (0, 0))

            if n >= 16:
                self.show(image, x, y)
                time.sleep(0.05)

        return image


app = App("Joconde_256.png")
