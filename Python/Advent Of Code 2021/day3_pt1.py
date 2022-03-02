nb_1 = [0] * 12
nb_lines = 1000

with open("day3_input.txt", "r") as f:
    for line in f.readlines():
        binary_num = line.strip()

        for i, car in enumerate(binary_num):
            nb_1[i] += 1 if car == "1" else 0

gamma = "".join("1" if nb > nb_lines / 2 else "0" for nb in nb_1)
epsilon = "".join("0" if car == "1" else "1" for car in gamma)

print(gamma, int(gamma, 2))
print(epsilon, int(epsilon, 2))
print(int(gamma, 2) * int(epsilon, 2))
