def len_sequence(n):
    length = 1
    while n != 1:
        n = (n / 2) if n % 2 == 0 else (3 * n + 1)
        length += 1
    return length


highest = 1
highest_starting = 1

for i in range(1, 1_000_000):
    if (length := len_sequence(i)) > highest:
        highest_starting = i
        highest = length

print(highest_starting)
