from huffman import *

with open("text2.txt", "r") as f:
    message = "".join(f.readlines())
    ab = arbre_huffman(frequence(message))

    code_binaire = code_huffman(message, ab)

with open("text2.bin", "w") as f:
    f.write(code_binaire)


# fichier original text.txt
# 2 167 737 octets
# = 17 341 896 bits

# fichier binaire text.bin
# 11 331 894 bits

# taux de compression : 0.34655968413

# ----------------------------------------

# fichier original text2.txt
# 13 899 600 octets
# = 111 196 800 bits

# fichier binaire text2.bin
# 13 899 600 bits

# taux de compression : 0.875
