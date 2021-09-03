
with open(input("Enter a file path: ")) as f: # f refers to the file
    lines = f.readlines() # getting all the lines stored in the 'lines' generator     
    for line in lines: # looping throw all the lines
        print(line)