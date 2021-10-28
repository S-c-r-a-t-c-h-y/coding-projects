Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c virtual_mouse.bat"
oShell.Run strArgs, 0, false