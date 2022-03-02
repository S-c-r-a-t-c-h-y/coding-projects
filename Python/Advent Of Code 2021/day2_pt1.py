position = depth = 0

with open("day2_input.txt", "r") as f:
    for line in f.readlines():
        action, amt = line.split(" ")
        if action == "forward":
            position += int(amt)
        elif action == "down":
            depth += int(amt)
        elif action == "up":
            depth -= int(amt)

print(position, depth, position * depth)
