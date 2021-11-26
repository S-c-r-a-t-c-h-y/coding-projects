@echo off
cls
:question
echo entrer le nom de la base :
set /p reponse=
if not exist %reponse% (
echo Cette base n'existe pas ! Verifier le nom du fichier.
timeout 3
cls
goto question
)
start sqlite3.exe -init .sqliterc %reponse%
