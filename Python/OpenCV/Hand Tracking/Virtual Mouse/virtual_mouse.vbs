Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c pythonw virtual_mouse.py"
oShell.Run strArgs, 0, false