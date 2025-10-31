import subprocess
import os
import pyautogui
from win10toast import ToastNotifier

class ActionExecutor:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.notifier = ToastNotifier()

    def execute_trigger(self, trigger_name):
        action = self.config.get('actions', {}).get(trigger_name)
        self.logger.info("Trigger %s => %s", trigger_name, action)
        if not action:
            return
        t = action.get('type')
        if t == 'builtin':
            fn = getattr(self, action['cmd'], None)
            if fn:
                fn()
        elif t == 'shell':
            cmd = action.get('cmd')
            subprocess.Popen(cmd, shell=True)
        elif t == 'python':
            fn = getattr(self, action['cmd'], None)
            if fn:
                fn()

    def abrir_vscode(self):
        possíveis = [
            r"C:\\Users\\dippf\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
            r"C:\\Program Files\\Microsoft VS Code\\Code.exe",
        ]
        for p in possíveis:
            if os.path.exists(p):
                subprocess.Popen([p])
                self.notifier.show_toast("Clap Assistant", "VS Code aberto", duration=3)
                return
        self.logger.warning("VSCode não encontrado.")

    def abrir_navegador(self):
        possíveis = [r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"]
        for p in possíveis:
            if os.path.exists(p):
                subprocess.Popen([p])
                return
        os.startfile("https://www.google.com")

    def bloquear_pc(self):
        subprocess.Popen("rundll32.exe user32.dll,LockWorkStation")

    def play_pause(self):
        pyautogui.press('playpause')
