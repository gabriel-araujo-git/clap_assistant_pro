import os, subprocess

def open_vscode():
    subprocess.Popen("code")
    return "Abrindo VS Code..."

def open_chrome():
    subprocess.Popen("chrome")
    return "Abrindo Google Chrome..."

def open_notepad():
    subprocess.Popen("notepad")
    return "Abrindo Bloco de Notas..."

def shutdown():
    os.system("shutdown /s /t 1")
    return "Desligando o computador..."

COMMANDS = {
    "vscode": open_vscode,
    "chrome": open_chrome,
    "bloco de notas": open_notepad,
    "computador": shutdown,
}
