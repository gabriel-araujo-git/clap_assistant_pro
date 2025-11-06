import customtkinter as ctk
import threading, subprocess, webbrowser, os
from pystray import Icon, MenuItem, Menu
from PIL import Image

# --- CommandEngine atualizado ---
class CommandEngine:
    def __init__(self):
        self.commands = {
            ("vscode", "code", "vs"): self.open_vscode,
            ("lnstudio", "ln", "aln", "lnstd", "std"): self.open_ln,
            ("ln teste", "alnteste", "lntst", "tst"): self.open_ln_tst,
            ("ln prd", "alnprd", "lnprod", "ln produção", "prd ln", "prd"): self.open_ln_prd,
            ("navegador", "chrome", "web"): self.open_browser,
        }

    def execute(self, text: str):
        text = text.lower().strip()
        text = text.replace("abrir o ", "").replace("abrir ", "").replace("entrar ", "")

        for keys, func in self.commands.items():
            if any(key in text for key in keys):
                return func()

        return f"Comando não reconhecido: {text}"

    def open_vscode(self):
        try:
            subprocess.Popen("code")
        except FileNotFoundError:
            vscode_path = r"C:\Users\107457\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk"
            if os.path.exists(vscode_path):
                subprocess.Popen(vscode_path, shell=True)
                return "Abrindo VSCode (via atalho)..."
            return "VSCode não encontrado."
        return "Abrindo VSCode..."

    def open_ln(self):
        subprocess.Popen(r"C:\LnStudio\eclipse\eclipse.exe")
        return "Abrindo LN Studio..."

    def open_ln_tst(self):
        webbrowser.open("https://mingle-portal.inforcloudsuite.com/v2/ELETROFRIO_TST/e6d06856-3c6a-44d9-8ce3-ed3affd6ab21")
        return "Abrindo ambiente de testes do LN..."

    def open_ln_prd(self):
        webbrowser.open("https://mingle-portal.inforcloudsuite.com/v2/ELETROFRIO_PRD/a8841f8a-7964-4977-b108-14edbb6ddb4f")
        return "Abrindo ambiente de produção do LN..."

    def open_browser(self):
        subprocess.Popen("chrome")
        return "Abrindo navegador..."


# --- Configurações da janela ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

engine = CommandEngine()  # 👈 usa o novo sistema de sinônimos

# --- Funções de ação ---
def executar_comando(comando):
    return engine.execute(comando)  # 👈 delega pro CommandEngine

# --- Interface principal ---
class AssistantApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Clap Assistant")
        self.geometry("300x150")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.input = ctk.CTkEntry(self, placeholder_text="Digite o comando...", width=250)
        self.input.pack(pady=20)
        self.input.bind("<Return>", self.on_enter)

        self.result = ctk.CTkLabel(self, text="")
        self.result.pack()

        self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def on_enter(self, event=None):
        cmd = self.input.get()
        result = executar_comando(cmd)
        self.result.configure(text=result)
        self.input.delete(0, "end")

    def hide_window(self):
        self.withdraw()

# --- Função para criar ícone de bandeja ---
def create_tray(app):
    def on_show(icon, item):
        app.deiconify()

    def on_quit(icon, item):
        icon.stop()
        app.destroy()

    image = Image.new("RGB", (64, 64), (0, 0, 255))
    menu = Menu(
        MenuItem("Mostrar assistente", on_show),
        MenuItem("Sair", on_quit)
    )
    icon = Icon("ClapAssistant", image, "Clap Assistant", menu)
    icon.run()

# --- Execução ---
if __name__ == "__main__":
    app = AssistantApp()
    tray_thread = threading.Thread(target=create_tray, args=(app,), daemon=True)
    tray_thread.start()
    app.mainloop()
