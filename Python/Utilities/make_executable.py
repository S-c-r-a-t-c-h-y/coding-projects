import os
import sys

args = sys.argv
print(args)
print(os.getcwd())

if "/v" in args or "/vbs" in args:
    with open(f"{'.'.join(args[1].split('.')[:-1])}.vbs", "w") as f:
        f.write('Set oShell = CreateObject ("Wscript.Shell")\n')
        f.write("Dim strArgs\n")
        f.write(f'strArgs = "cmd /c pythonw {args[1]}"\n')
        f.write("oShell.Run strArgs, 0, false")
else:
    with open(f"{'.'.join(args[1].split('.')[:-1])}.bat", "w") as f:
        f.write(f"python {args[1]}")
