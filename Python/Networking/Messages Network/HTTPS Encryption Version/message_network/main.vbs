Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c pythonw main.py"
oShell.Run strArgs, 0, false