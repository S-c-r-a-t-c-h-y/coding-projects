def is_palindrome_number(n):
    return str(n) == str(n)[::-1]


highest = 0
for i in range(1000):
    for j in range(1000):
        if is_palindrome_number((res := i * j)):
            highest = max(highest, res)

print(highest)
