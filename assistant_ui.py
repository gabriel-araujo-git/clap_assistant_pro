import customtkinter as ctk
import threading, subprocess, webbrowser, os
from pystray import Icon, MenuItem, Menu
from PIL import Image

# --- Configurações da janela ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- Funções de ação ---
def executar_comando(comando):
    comando = comando.lower().strip()

    # --- comandos personalizados ---
    if "vscode" in comando:
        subprocess.Popen("code")
        return "Abrindo VSCode..."
    
    elif "ln" in comando and "teste" in comando:
        webbrowser.open("https://mingle-portal.inforcloudsuite.com/v2/ELETROFRIO_TST/e6d06856-3c6a-44d9-8ce3-ed3affd6ab21")
        return "Abrindo ambiente de testes do LN..."
    
    elif "ln" in comando and "prd" in comando:
        webbrowser.open("https://mingle-portal.inforcloudsuite.com/v2/ELETROFRIO_PRD/a8841f8a-7964-4977-b108-14edbb6ddb4f")
        return "Abrindo ambiente de produção do LN..."
    
    elif "ln" in comando:
        subprocess.Popen(r"C:\LnStudio\eclipse\eclipse.exe")
        return "Abrindo LN Studio..."

    elif "navegador" in comando or "chrome" in comando:
        subprocess.Popen("chrome")
        return "Abrindo navegador..."

    else:
        return "Comando não reconhecido."

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
