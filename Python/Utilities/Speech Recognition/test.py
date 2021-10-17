import os
cmd = "synchronise le code sur github avec le message ajouts de commande de reconnaissance vocale"

if set(["synchronise", "code", "github"]).issubset(commande := cmd.split(" ")):
    msg = ""
    if set(["avec", "le", "message"]).issubset(commande):
        msg = " ".join(commande).split("message ")[-1]
    current = os.getcwd()
    os.chdir(r"C:\Users\Personne\Desktop\'Coding Projects'")
    os.system("git add .")
    os.system(f'git commit -m "{msg}"')
    os.system("git push")
    os.chdir(current)