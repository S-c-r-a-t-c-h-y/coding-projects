from PIL import Image

im2 = Image.open("Joconde_256.png")


def rotation(image):
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
        a = rotation(a)
        b = rotation(b)
        c = rotation(c)
        d = rotation(d)
        # Combiner : permutation des blocs
        image.paste(a, (k, k))
        image.paste(b, (0, k))
        image.paste(c, (0, 0))
        image.paste(d, (k, 0))

    return image


rotation(im2)
im2.save("joconde4.png", "PNG")
