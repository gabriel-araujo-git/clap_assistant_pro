# assistant_ui.py
import customtkinter as ctk
import threading
import subprocess
import webbrowser
import os
from pystray import Icon, MenuItem, Menu
from PIL import Image

# ---------------------------
# CommandEngine (sinônimos)
# ---------------------------
class CommandEngine:
    def __init__(self):
        # cada tuple são sinônimos/abreviações que mapeiam para a mesma ação
        self.commands = {
            # VSCode
            ("abrir vscode", "vscode", "code", "vs", "abrir code", "abrir vs", "open vscode"): self.open_vscode,

            # LN Studio (local)
            ("abrir ln", "ln", "lnstudio", "studio ln", "aln", "lnstd", "std", "abrir ln studio"): self.open_ln,

            # LN Teste (web)
            ("abrir ln teste", "ln teste", "alnteste", "teste ln", "lntst", "ln tst", "ln-test", "TST", "tst"): self.open_ln_tst,

            # LN Produção (web)
            ("abrir ln prd", "ln prd", "alnprd", "lnprod", "ln produção", "prd ln", "ln-prd", "PRD", "prd"): self.open_ln_prd,

            # Navegador / Chrome / web
            ("abrir navegador", "abrir chrome", "navegador", "chrome", "abrir web", "open browser", "browser", "web"): self.open_browser,

            # Exemplos adicionais (você pode adicionar aqui)
            ("abrir explorer", "explorer", "explorar", "abrir explorador", "abrir explorador de arquivos"): self.open_explorer,
            ("bloco de notas", "notepad", "abrir notepad", "abrir bloco de notas"): self.open_notepad,
        }

    def normalize(self, text: str) -> str:
        t = text.lower().strip()
        # remove palavras comuns que só atrapalham ("abrir", "abrir o", "entrar em" etc.)
        replacements = ["abrir o ", "abrir a ", "abrir ", "entrar em ", "entrar no ", "por favor ", "por favor, "]
        for r in replacements:
            t = t.replace(r, "")
        # collapse whitespace
        t = " ".join(t.split())
        return t

    def execute(self, text: str) -> str:
        text = self.normalize(text)
        # procura se algum sinônimo está contido na string
        for keys, func in self.commands.items():
            for key in keys:
                if key in text:
                    try:
                        return func()
                    except Exception as e:
                        return f"❌ Erro ao executar: {e}"
        return f"❓ Comando não reconhecido: '{text}'"

    # ---------------------------
    # Ações (retornam mensagem)
    # ---------------------------
    def open_vscode(self) -> str:
        # tenta abrir via comando 'code' (se instalado no PATH)
        try:
            subprocess.Popen("code", shell=True)
            return "🚀 Abrindo VSCode..."
        except Exception:
            # fallback para atalho do menu iniciar (lnk) ou executável
            possible = [
                r"C:\Users\107457\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk",
                r"C:\Program Files\Microsoft VS Code\Code.exe",
                r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
            ]
            for p in possible:
                if os.path.exists(p):
                    try:
                        subprocess.Popen(p, shell=True)
                        return "🚀 Abrindo VSCode (fallback)..."
                    except Exception:
                        continue
            return "❌ VSCode não encontrado. Verifique a instalação ou adicione 'code' ao PATH."

    def open_ln(self) -> str:
        # ajuste o caminho se necessário
        ln_path = r"C:\LnStudio\eclipse\eclipse.exe"
        if os.path.exists(ln_path):
            subprocess.Popen(ln_path, shell=True)
            return "🦾 Abrindo LN Studio..."
        else:
            return f"❌ LN Studio não encontrado em: {ln_path}"

    def open_ln_tst(self) -> str:
        url = "https://mingle-portal.inforcloudsuite.com/v2/ELETROFRIO_TST/e6d06856-3c6a-44d9-8ce3-ed3affd6ab21"
        webbrowser.open(url)
        return "🧪 Abrindo ambiente de testes do LN..."

    def open_ln_prd(self) -> str:
        url = ("https://mingle-portal.inforcloudsuite.com/v2/ELETROFRIO_PRD/"
               "a8841f8a-7964-4977-b108-14edbb6ddb4f")
        webbrowser.open(url)
        return "🏭 Abrindo ambiente de produção do LN..."

    def open_browser(self) -> str:
        # tenta abrir chrome; se não, abre navegador padrão via webbrowser
        try:
            subprocess.Popen("chrome", shell=True)
            return "🌐 Abrindo Chrome..."
        except Exception:
            webbrowser.open("https://www.google.com")
            return "🌐 Abrindo navegador padrão..."

    def open_explorer(self) -> str:
        try:
            subprocess.Popen("explorer", shell=True)
            return "📁 Abrindo Explorador de Arquivos..."
        except Exception:
            return "❌ Erro ao abrir explorador."

    def open_notepad(self) -> str:
        possible = ["notepad.exe", r"C:\Windows\system32\notepad.exe"]
        for p in possible:
            try:
                subprocess.Popen(p, shell=True)
                return "📝 Abrindo Bloco de Notas..."
            except Exception:
                continue
        return "❌ Bloco de notas não encontrado."

# ---------------------------
# UI: Lynx (customtkinter)
# ---------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

engine = CommandEngine()

class LynxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lynx")
        self.geometry("360x180")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#0f1113")

        # título
        self.label_title = ctk.CTkLabel(
            self,
            text="🦊 Lynx",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2db7ff"
        )
        self.label_title.pack(pady=(12, 6))

        # entrada com autocomplete visual simples (placeholder)
        self.input = ctk.CTkEntry(
            self,
            placeholder_text="Digite o comando (ex: 'ln teste', 'vscode')",
            width=320,
            height=36,
            corner_radius=10
        )
        self.input.pack(pady=(6, 8))
        self.input.bind("<Return>", self.on_enter)
        # history simples (setas)
        self.history = []
        self.history_index = None
        self.input.bind("<Up>", self.on_history_up)
        self.input.bind("<Down>", self.on_history_down)

        # resultado
        self.result = ctk.CTkLabel(
            self,
            text="",
            text_color="#d0d0d0",
            font=ctk.CTkFont(size=13)
        )
        self.result.pack(pady=(2, 10))

        # botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 8))
        self.btn_close = ctk.CTkButton(btn_frame, text="Fechar", width=80, command=self.hide_window)
        self.btn_close.grid(row=0, column=0, padx=6)
        self.btn_help = ctk.CTkButton(btn_frame, text="Ajuda", width=80, command=self.show_help)
        self.btn_help.grid(row=0, column=1, padx=6)

        self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def on_enter(self, event=None):
        cmd = self.input.get().strip()
        if not cmd:
            return
        # salva no histórico
        self.history.append(cmd)
        self.history_index = None

        result = engine.execute(cmd)
        self.result.configure(text=result)
        self.input.delete(0, "end")

    def hide_window(self):
        self.withdraw()

    def show_help(self):
        # janela de ajuda simples
        from tkinter import Toplevel, Label
        h = Toplevel(self)
        h.title("Lynx - Comandos rápidos")
        h.geometry("420x260")
        h.attributes("-topmost", True)
        txt = (
            "Comandos suportados (exemplos):\n\n"
            "- vscode / code / vs / abrir vscode\n"
            "- ln / lnstudio / studio ln / abrir ln\n"
            "- ln teste / alnteste / lntst\n"
            "- ln prd / lnprod / alnprd\n"
            "- navegador / chrome / web\n"
            "- explorer / abrir explorer\n"
            "- bloco de notas / notepad\n\n"
            "Dica: você pode usar abreviações ou escrever 'abrir ln teste'.\n"
            "Adicione sinônimos editando CommandEngine.commands no código."
        )
        Label(h, text=txt, justify="left", padx=12, pady=12).pack()

    # history navigation
    def on_history_up(self, event=None):
        if not self.history:
            return
        if self.history_index is None:
            self.history_index = len(self.history) - 1
        elif self.history_index > 0:
            self.history_index -= 1
        self.input.delete(0, "end")
        self.input.insert(0, self.history[self.history_index])

    def on_history_down(self, event=None):
        if not self.history or self.history_index is None:
            return
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.input.delete(0, "end")
            self.input.insert(0, self.history[self.history_index])
        else:
            self.history_index = None
            self.input.delete(0, "end")

# ---------------------------
# tray icon
# ---------------------------
def create_tray(app):
    def on_show(icon, item):
        app.deiconify()

    def on_quit(icon, item):
        icon.stop()
        try:
            app.destroy()
        except Exception:
            pass

    image = Image.new("RGB", (64, 64), (0, 153, 255))
    menu = Menu(MenuItem("Mostrar Lynx", on_show), MenuItem("Sair", on_quit))
    icon = Icon("Lynx", image, "Lynx Assistant", menu)
    icon.run()

# ---------------------------
# run
# ---------------------------
if __name__ == "__main__":
    app = LynxApp()
    tray_thread = threading.Thread(target=create_tray, args=(app,), daemon=True)
    tray_thread.start()
    app.mainloop()
