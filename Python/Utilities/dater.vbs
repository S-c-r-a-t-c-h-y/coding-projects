Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c pythonw dater.py"
oShell.Run strArgs, 0, false