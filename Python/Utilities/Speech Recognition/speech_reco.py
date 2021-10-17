import speech_recognition as sr
import time
import os, sys

paths = {
    "global": r"C:\Users\Personne\Desktop\Coding Projects",
    "python": r"C:\Users\Personne\Desktop\Coding Projects\Python",
}

def evaluer_commande(commande):
    """ fonction qui prend une commande comme argument et qui analyse puis execute son contenu"""
    print(commande)
    parts = commande.split(" ")

    commandes = {
        "ouvre python usb": [r"code D:\NSI"],
        "ouvre python pc": [r"code C:\Users\Personne\Desktop\'Coding Projects'\Python"],

        "ouvre google" : ["start chrome"],
        "ouvre naviguateur" : ["start chrome"],
        "ouvre github": ["start https://github.com/S-c-r-a-t-c-h-y/coding-projects"],

        "ouvre visual studio code" : ["code"],
        "ouvre vs code" : ["code"],

        "ouvre discorde": ['discord'],

        "ferme-toi": ["shutdown /s /t 10"],
        "ferme toi": ["shutdown /s /t 10"],
        "annule fermeture": ["shutdown /a"],
        "redémarre": ["shutdown /g"],
        "mets-toi en veille": ["shutdown /h"],
        "veille": ["shutdown /h"],
        "verrouille toi": ["shutdown /l"],
        
        "synchroniser clé usb": [r'xcopy /E /I "D:\NSI" "C:\Users\Personne\Desktop\Coding Projects\NSI"'],
        "synchronise clé usb": [r'xcopy /E /I "D:\NSI" "C:\Users\Personne\Desktop\Coding Projects\NSI"'],

    }

    if commande in ["arrête la reconnaissance", "stop"]:
        raise KeyboardInterrupt

    elif set(["cherche", "sur", "google"]).issubset(cmd := commande.split(" ")):
        cmd = "+".join(cmd[1:len(cmd)-2])
        os.system(f'start https://www.google.com/search?q={cmd}')

    elif set(["cherche", "sur", "youtube"]).issubset(cmd := commande.split(" ")):
        cmd = "+".join(cmd[1:len(cmd)-2])
        os.system(f"start https://www.youtube.com/results?search_query={cmd}")

    elif set(["cherche", "sur", "spotify"]).issubset(cmd := commande.split(" ")):
        cmd = "%20".join(cmd[1:len(cmd)-2])
        os.system(f"start https://open.spotify.com/search/{cmd}")
        
    elif set(["synchronise", "github"]).issubset(cmd := commande.split(" ")) or set(["synchroniser", "github"]).issubset(cmd):
        msg = ""
        if set(["message"]).issubset(cmd):
            msg = " ".join(cmd).split("message ")[-1]
        current = os.getcwd()
        os.chdir(paths["global"])
        os.system("git add .")
        os.system(f'git commit -m "{msg}"')
        os.system("git push")
        os.chdir(current)

    elif commande in commandes:
        for c in commandes[commande]:
            os.system(c)

    elif parts[0] == "ouvre":
        os.system(f'start {" ".join(parts[1:])}')

text = ""
prev_text = text

def callback(recognizer, audio):
    global text
    try:
        text = recognizer.recognize_google(audio, language='fr-FR')
    except sr.RequestError:
        pass
    except sr.UnknownValueError:
        pass

r = sr.Recognizer()
r.energy_threshold = 300
r.pause_threshold = 0.5
mic = sr.Microphone()
keyword = "ordi"

with mic as source:
    r.adjust_for_ambient_noise(source)

stop_listening = r.listen_in_background(mic, callback)

print("Starting recognition.")

try:
    while True:
        
        if text != prev_text and keyword.lower() in text.lower():
            commande = text.split(keyword)[1]

            if commande.startswith("s "):
                commande = commande[2:]
            elif commande.startswith(" "):
                commande = commande[1:]

            evaluer_commande(commande.lower())

        prev_text = text

        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped listening.")

stop_listening()