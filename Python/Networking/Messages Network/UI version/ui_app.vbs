Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs = "cmd /c pythonw ui_app.py"
oShell.Run strArgs, 0, false