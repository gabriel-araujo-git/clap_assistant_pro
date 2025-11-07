# lynx_insideof.py
"""
Lynx (Insideof Edition)
- Delivery: .py (runs on Windows)
- Contextual "insideof" mode (currently supports: vscode)
- Shows context indicator in the UI
- Uses pyautogui for simple editor automation

Dependencies:
    pip install customtkinter pyautogui psutil pystray pillow

Run:
    python lynx_insideof.py
"""
import customtkinter as ctk
import threading
import subprocess
import webbrowser
import os
import json
import pyautogui
import psutil
import time
from pystray import Icon, MenuItem, Menu
from PIL import Image
from tkinter import filedialog, messagebox

# ---------------------------
# CommandEngine
# ---------------------------
class CommandEngine:
    def __init__(self):
        self.context = None  # contexto ativo (ex: 'vscode')
        self.commands = {}
        self.context_actions = {}

<<<<<<< HEAD
        # comandos gerais e contextuais
        self.register_default_commands()
        self.register_context_actions()

        # carrega comandos personalizados (mantém compatibilidade)
=======
        # sites fixos
        self.commands.update({
            # 🌐 Redes sociais
            ("abrir instagram", "instagram", "insta"): lambda: self.open_site("https://www.instagram.com"),
            ("abrir facebook", "facebook", "face", "fb"): lambda: self.open_site("https://www.facebook.com"),
            ("abrir twitter", "twitter", "x", "x.com"): lambda: self.open_site("https://x.com"),
            ("abrir tiktok", "tiktok", "tt"): lambda: self.open_site("https://www.tiktok.com"),
            ("abrir whatsapp", "whatsapp", "zap"): lambda: self.open_site("https://web.whatsapp.com"),
            ("abrir discord", "discord", "dc"): lambda: self.open_site("https://discord.com"),
            ("abrir telegram", "telegram", "tg"): lambda: self.open_site("https://web.telegram.org"),
            ("abrir linkedin", "linkedin", "lnkd"): lambda: self.open_site("https://www.linkedin.com"),
            ("abrir reddit", "reddit", "rdt"): lambda: self.open_site("https://www.reddit.com"),
            ("abrir snapchat", "snapchat", "snap"): lambda: self.open_site("https://www.snapchat.com"),

            # 🎬 Streaming e música
            ("abrir youtube", "youtube", "yt"): lambda: self.open_site("https://www.youtube.com"),
            ("abrir netflix", "netflix", "nfx"): lambda: self.open_site("https://www.netflix.com"),
            ("abrir spotify", "spotify", "spot"): lambda: self.open_site("https://www.spotify.com"),
            ("abrir twitch", "twitch", "tw"): lambda: self.open_site("https://www.twitch.tv"),
            ("abrir prime video", "prime", "primevideo"): lambda: self.open_site("https://www.primevideo.com"),
            ("abrir hbo max", "hbomax", "hbo"): lambda: self.open_site("https://www.hbomax.com"),
            ("abrir disney plus", "disneyplus", "disney+"): lambda: self.open_site("https://www.disneyplus.com"),
            ("abrir crunchyroll", "crunchyroll", "anime"): lambda: self.open_site("https://www.crunchyroll.com"),
            ("abrir paramount plus", "paramountplus", "paramount"): lambda: self.open_site("https://www.paramountplus.com"),
            ("abrir star plus", "starplus", "star+"): lambda: self.open_site("https://www.starplus.com"),

            # 💼 Produtividade
            ("abrir google drive", "drive", "gdrive"): lambda: self.open_site("https://drive.google.com"),
            ("abrir google docs", "docs", "gdocs"): lambda: self.open_site("https://docs.google.com"),
            ("abrir notion", "notion"): lambda: self.open_site("https://www.notion.so"),
            ("abrir canva", "canva"): lambda: self.open_site("https://www.canva.com"),
            ("abrir trello", "trello"): lambda: self.open_site("https://trello.com"),
            ("abrir microsoft 365", "office", "microsoft"): lambda: self.open_site("https://www.microsoft365.com"),
            ("abrir slack", "slack"): lambda: self.open_site("https://www.slack.com"),
            ("abrir todoist", "todoist"): lambda: self.open_site("https://todoist.com"),
            ("abrir dropbox", "dropbox"): lambda: self.open_site("https://www.dropbox.com"),
            ("abrir google agenda", "calendar", "agenda"): lambda: self.open_site("https://calendar.google.com"),

            # 💰 Bancos e pagamentos
            ("abrir nubank", "nubank", "nu"): lambda: self.open_site("https://nubank.com.br"),
            ("abrir itau", "itau"): lambda: self.open_site("https://www.itau.com.br"),
            ("abrir banco do brasil", "bb", "bancobb"): lambda: self.open_site("https://www.bb.com.br"),
            ("abrir caixa", "caixa", "cef"): lambda: self.open_site("https://www.caixa.gov.br"),
            ("abrir picpay", "picpay"): lambda: self.open_site("https://www.picpay.com"),
            ("abrir paypal", "paypal"): lambda: self.open_site("https://www.paypal.com"),
            ("abrir mercado pago", "mercadopago", "mp"): lambda: self.open_site("https://www.mercadopago.com.br"),
            ("abrir santander", "santander"): lambda: self.open_site("https://www.santander.com.br"),
            ("abrir banco inter", "inter"): lambda: self.open_site("https://inter.co"),
            ("abrir banco pan", "pan"): lambda: self.open_site("https://www.bancopan.com.br"),

            # 🧠 Estudos e pesquisa
            ("abrir chatgpt", "chatgpt", "gpt"): lambda: self.open_site("https://chat.openai.com"),
            ("abrir google scholar", "scholar", "acadêmico"): lambda: self.open_site("https://scholar.google.com"),
            ("abrir khan academy", "khanacademy", "khan"): lambda: self.open_site("https://www.khanacademy.org"),
            ("abrir coursera", "coursera"): lambda: self.open_site("https://www.coursera.org"),
            ("abrir udemy", "udemy"): lambda: self.open_site("https://www.udemy.com"),
            ("abrir wikipedia", "wikipedia", "wiki"): lambda: self.open_site("https://www.wikipedia.org"),
            ("abrir mendeley", "mendeley"): lambda: self.open_site("https://www.mendeley.com"),
            ("abrir perplexity", "perplexity"): lambda: self.open_site("https://www.perplexity.ai"),
            ("abrir codecademy", "codecademy"): lambda: self.open_site("https://www.codecademy.com"),
            ("abrir tradutor", "translate", "google tradutor"): lambda: self.open_site("https://translate.google.com"),

            # ⚙️ Programas internos
            ("abrir bloco de notas", "notepad", "bloco"): lambda: subprocess.Popen("notepad.exe", shell=True),
            ("abrir calculadora", "calc", "calculadora"): lambda: subprocess.Popen("calc.exe", shell=True),
            ("abrir paint", "paint", "pintar"): lambda: subprocess.Popen("mspaint.exe", shell=True),
            ("abrir explorador", "explorer", "explorar"): lambda: subprocess.Popen("explorer.exe", shell=True),
            ("abrir prompt", "cmd", "prompt"): lambda: subprocess.Popen("cmd.exe", shell=True),
            ("abrir powershell", "powershell"): lambda: subprocess.Popen("powershell.exe", shell=True),
            ("abrir word", "word"): lambda: subprocess.Popen("winword.exe", shell=True),
            ("abrir excel", "excel", "planilha"): lambda: subprocess.Popen("excel.exe", shell=True),
            ("abrir powerpoint", "powerpoint", "ppt"): lambda: subprocess.Popen("powerpnt.exe", shell=True),
            ("abrir vscode", "vscode", "code", "vs"): lambda: subprocess.Popen("code", shell=True),
            ("abrir navegador", "chrome", "browser"): lambda: subprocess.Popen("chrome", shell=True),
            ("abrir painel de controle", "control", "painel"): lambda: subprocess.Popen("control.exe", shell=True),
            ("abrir task manager", "gerenciador", "tarefas", "taskmgr"): lambda: subprocess.Popen("taskmgr.exe", shell=True),
            ("abrir config", "configurações", "settings"): lambda: subprocess.Popen("start ms-settings:", shell=True),

            # 🔒 Atalhos de sistema
            ("bloquear computador", "bloquear", "lock"): lambda: os.system("rundll32.exe user32.dll,LockWorkStation"),
            ("reiniciar computador", "reiniciar", "restart", "reboot"): lambda: os.system("shutdown /r /t 0"),
            ("desligar computador", "desligar", "shutdown", "poweroff"): lambda: os.system("shutdown /s /t 0"),
            ("hibernar", "suspender", "sleep"): lambda: os.system("shutdown /h"),
            ("abrir downloads", "downloads"): lambda: subprocess.Popen(f"explorer.exe {os.path.expanduser('~/Downloads')}", shell=True),
            ("abrir documentos", "documentos"): lambda: subprocess.Popen(f"explorer.exe {os.path.expanduser('~/Documents')}", shell=True),
            ("abrir imagens", "imagens", "pictures"): lambda: subprocess.Popen(f"explorer.exe {os.path.expanduser('~/Pictures')}", shell=True),
            ("abrir vídeos", "videos", "movies"): lambda: subprocess.Popen(f"explorer.exe {os.path.expanduser('~/Videos')}", shell=True),
            ("abrir área de trabalho", "desktop"): lambda: subprocess.Popen(f"explorer.exe {os.path.expanduser('~/Desktop')}", shell=True),
        })


        # carrega comandos personalizados
>>>>>>> 1af2b3e86c591ccdca5a294d90673f0f6d8aee4c
        self.load_custom_commands()

    # ---------------------------
    # Registro de comandos
    # ---------------------------
    def register_default_commands(self):
        self.commands.update({
            # apps comuns
            ("abrir vscode", "vscode", "code"): lambda: self.open_app("code"),
            ("abrir navegador", "chrome", "browser"): lambda: subprocess.Popen("chrome", shell=True),
            ("abrir explorer", "explorer"): lambda: subprocess.Popen("explorer", shell=True),
            ("abrir notepad", "notepad", "bloco de notas"): lambda: subprocess.Popen("notepad.exe", shell=True),

            # sites fixos
            ("youtube", "abrir youtube"): lambda: self.open_site("https://youtube.com"),
            ("github", "abrir github"): lambda: self.open_site("https://github.com"),
            ("google", "abrir google"): lambda: self.open_site("https://google.com"),

            # sair do contexto (comando global também)
            ("sair", "exit"): self.exit_context,
        })

    def register_context_actions(self):
        # ações contextuais por aplicativo (atualmente: vscode)
        self.context_actions = {
            "vscode": {
                ("novo arquivo", "criar arquivo", "new file"): lambda: self.vscode_key("ctrl", "n"),
                ("salvar", "save", "salvar arquivo"): lambda: self.vscode_key("ctrl", "s"),
                ("executar script", "rodar script", "run"): lambda: self.vscode_key("ctrl", "f5"),
                ("fechar aba", "close tab", "fechar"): lambda: self.vscode_key("ctrl", "w"),
            }
        }

    def load_custom_commands(self):
        """Carrega comandos personalizados"""
        try:
            with open("commands.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            for cmd in data.get("commands", []):
                if cmd.get("type") == "internal":
                    func = lambda path=cmd.get("path"): subprocess.Popen(path, shell=True)
                elif cmd.get("type") == "external":
                    func = lambda url=cmd.get("url"): webbrowser.open(url)
                else:
                    continue
                self.commands[tuple(cmd.get("keywords", []))] = func
        except FileNotFoundError:
            with open("commands.json", "w", encoding="utf-8") as f:
                json.dump({"commands": []}, f, indent=4, ensure_ascii=False)

    # ---------------------------
    # Execução de comandos
    # ---------------------------
    def normalize(self, text: str) -> str:
        t = text.lower().strip()
        for r in ["abrir o ", "abrir a ", "abrir ", "entrar em ", "entrar no ", "por favor ", "por favor, "]:
            t = t.replace(r, "")
        return " ".join(t.split())

    def execute(self, text: str) -> str:
        text = self.normalize(text)

        # 1) Se o comando for "insideof <app>"
        if text.startswith("insideof "):
            app = text.split(" ", 1)[1].strip()
            return self.enter_context(app)

        # 2) Se estiver em modo insideof, tente as ações contextuais primeiro
        if self.context:
            actions = self.context_actions.get(self.context, {})
            for keys, func in actions.items():
                if any(key in text for key in keys):
                    try:
                        func()
                        return f"⚙️ Executando '{text}' dentro de {self.context.capitalize()}"
                    except Exception as e:
                        return f"❌ Erro ao executar ação no contexto: {e}"
            # permitir sair do contexto com palavras-chave globais
            if text in ("sair", "exit"):
                return self.exit_context()
            return f"💡 Você está dentro de {self.context.capitalize()}. Comando não reconhecido para este contexto."

        # 3) Comandos gerais / fora de contexto
        for keys, func in self.commands.items():
            for key in keys:
                if key in text:
                    try:
                        result = func()
                        # se a função retornar string, repassa; senão, devolve uma mensagem padrão
                        return result if isinstance(result, str) else f"✅ Executando: {key}"
                    except Exception as e:
                        return f"❌ Erro ao executar: {e}"

        return f"❓ Comando não reconhecido: '{text}'"

    # ---------------------------
    # Contexto universal
    # ---------------------------
    def enter_context(self, app: str) -> str:
        app = app.lower()
        supported = ("vscode",)  # por ora apenas vscode
        if app not in supported:
            return f"❌ Aplicação '{app}' não suportada. Suportado: {', '.join(supported)}"

        # abre app se não estiver aberto
        if not self.is_process_running(app):
            self.open_app(app)
            # tempo para abrir (pode ajustar)
            time.sleep(2.5)

        self.context = app
        return f"💡 Agora você está dentro do {app.capitalize()} (modo insideof ativo)."

    def exit_context(self) -> str:
        if not self.context:
            return "ℹ️ Nenhum contexto ativo."
        prev = self.context
        self.context = None
        return f"⬅️ Saiu do modo insideof ({prev})."

    # ---------------------------
    # Utilitários
    # ---------------------------
    def is_process_running(self, name: str) -> bool:
        name = name.lower()
        for proc in psutil.process_iter(["name"]):
            try:
                if proc.info["name"] and name in proc.info["name"].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def open_app(self, name: str):
        try:
            # mapeamento simples: 'vscode' -> 'code' CLI
            if name == "vscode":
                subprocess.Popen("code", shell=True)
            else:
                subprocess.Popen(name, shell=True)
        except Exception:
            pass

    def open_site(self, url: str):
        webbrowser.open(url)

    # ---------------------------
    # Ações específicas por app
    # ---------------------------
    def vscode_key(self, *keys):
        """
        Envia atalho de teclado para o VSCode via pyautogui.
        Nota: pyautogui envia para a janela com foco.
        """
        try:
            pyautogui.hotkey(*keys)
            time.sleep(0.2)
        except Exception as e:
            raise e

# ---------------------------
# UI: Lynx
# ---------------------------
# ---------------------------
# UI: Lynx (versão aprimorada)
# ---------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

engine = CommandEngine()

class LynxApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Lynx")
        self.geometry("420x220")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#0f1113")

<<<<<<< HEAD
        # título
        self.label_title = ctk.CTkLabel(self, text="Lynx", font=ctk.CTkFont(size=20, weight="bold"), text_color="#2db7ff")
        self.label_title.pack(pady=(12, 6))

        # entrada
        self.input = ctk.CTkEntry(self, placeholder_text="Digite o comando (ex: 'insideof vscode' ou 'novo arquivo')", width=380, height=36)
        self.input.pack(pady=(6, 6))
        self.input.bind("<Return>", self.on_enter)

        # indicador de contexto
        self.context_label = ctk.CTkLabel(self, text="Contexto: —", text_color="#bdbdbd", font=ctk.CTkFont(size=12))
        self.context_label.pack(pady=(2, 8))

        # resultado
        self.result = ctk.CTkLabel(self, text="", text_color="#d0d0d0", font=ctk.CTkFont(size=13))
        self.result.pack(pady=(2, 10))
=======
        # ---------------------------
        # Header com ícone e título
        # ---------------------------
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(pady=(10, 4))

        # círculo simbólico (ícone)
        self.icon_canvas = ctk.CTkCanvas(header, width=14, height=14, bg="#0f1113", highlightthickness=0)
        self.icon_canvas.create_oval(2, 2, 12, 12, fill="#2db7ff", outline="")
        self.icon_canvas.pack(side="left", padx=(0, 6))

        # título com glow
        self.label_title = ctk.CTkLabel(
            header,
            text="Lynx",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#2db7ff"
        )
        self.label_title.pack(side="left")

        # ---------------------------
        # Entrada
        # ---------------------------
        self.input = ctk.CTkEntry(
            self,
            placeholder_text="Digite o comando (ex: 'ln teste', 'vscode')",
            width=320,
            height=36,
            border_width=2,
            corner_radius=8
        )
        self.input.pack(pady=(10, 8))
        self.input.bind("<Return>", self.on_enter)

        # ---------------------------
        # Resultado
        # ---------------------------
        self.result = ctk.CTkLabel(
            self,
            text="",
            text_color="#d0d0d0",
            font=ctk.CTkFont(size=13)
        )
        self.result.pack(pady=(4, 10))
>>>>>>> 1af2b3e86c591ccdca5a294d90673f0f6d8aee4c

        # ---------------------------
        # Botões
        # ---------------------------
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 8))

        self.btn_close = ctk.CTkButton(btn_frame, text="Fechar", width=80, command=self.hide_window)
        self.btn_close.grid(row=0, column=0, padx=6)
        self.btn_help = ctk.CTkButton(btn_frame, text="Ajuda", width=80, command=self.show_help)
        self.btn_help.grid(row=0, column=1, padx=6)
        self.btn_add = ctk.CTkButton(btn_frame, text="Adicionar", width=80, command=self.show_add_command)
        self.btn_add.grid(row=0, column=2, padx=6)

        self.protocol("WM_DELETE_WINDOW", self.hide_window)

<<<<<<< HEAD
        # atualiza indicador ao iniciar
        self.update_context_label()

=======
        # animação do ícone
        self.animate_icon()

    # ---------------------------
    # Animação: ícone pulsante
    # ---------------------------
    def animate_icon(self):
        import math, time
        t = time.time() * 2.5
        brightness = 0.6 + 0.4 * math.sin(t)
        color = f'#{int(45 * brightness):02x}{int(183 * brightness):02x}{int(255 * brightness):02x}'
        self.icon_canvas.delete("all")
        self.icon_canvas.create_oval(2, 2, 12, 12, fill=color, outline="")
        self.after(100, self.animate_icon)

    # ---------------------------
    # Evento Enter
    # ---------------------------
>>>>>>> 1af2b3e86c591ccdca5a294d90673f0f6d8aee4c
    def on_enter(self, event=None):
        cmd = self.input.get().strip()
        if not cmd:
            return
        result = engine.execute(cmd)
<<<<<<< HEAD
        # se o engine mudou o contexto, atualizar o label
        self.update_context_label()
        self.result.configure(text=result)
=======
        self.show_result_feedback(result)
>>>>>>> 1af2b3e86c591ccdca5a294d90673f0f6d8aee4c
        self.input.delete(0, "end")

    # ---------------------------
    # Feedback visual
    # ---------------------------
    def show_result_feedback(self, text):
        self.result.configure(text=text, text_color="#2db7ff")
        self.after(100, lambda: self.result.configure(text_color="#d0d0d0"))

    # ---------------------------
    # Outros métodos
    # ---------------------------
    def hide_window(self):
        self.withdraw()

    def show_help(self):
        from tkinter import Toplevel, Label
        h = Toplevel(self)
        h.title("Lynx - Comandos rápidos")
        h.geometry("520x300")
        h.attributes("-topmost", True)
        txt = (
            "Comandos padrão (exemplos):\n\n"
            "- insideof vscode         -> entra no modo interno do VSCode\n"
            "- novo arquivo / salvar   -> comandos que funcionam dentro do VSCode (quando em contexto)\n"
            "- executar script         -> rodar (Ctrl+F5) dentro do VSCode\n"
            "- sair / exit             -> sai do contexto\n\n"
            "💡 Você pode adicionar novos comandos pelo botão 'Adicionar' (comandos externos ou internos simples)."
        )
        Label(h, text=txt, justify="left", padx=12, pady=12).pack()

    def show_add_command(self):
        # igual à sua versão original
        from tkinter import Toplevel, Label, Entry, Button, Radiobutton, StringVar, filedialog, messagebox
        win = Toplevel(self)
        win.title("Adicionar Comando")
        win.geometry("380x360")
        win.configure(bg="#1b1d1f")
        win.attributes("-topmost", True)
        Label(win, text="Tipo de comando:", fg="white", bg="#1b1d1f").pack(pady=4)
        cmd_type = StringVar(value="internal")
        Radiobutton(win, text="Interno (programa)", variable=cmd_type, value="internal", bg="#1b1d1f", fg="white").pack()
        Radiobutton(win, text="Externo (site)", variable=cmd_type, value="external", bg="#1b1d1f", fg="white").pack()
        Label(win, text="Nome do comando:", fg="white", bg="#1b1d1f").pack(pady=(8, 2))
        name_entry = Entry(win, width=40)
        name_entry.pack()
        Label(win, text="Palavras-chave (separadas por vírgula):", fg="white", bg="#1b1d1f").pack(pady=(8, 2))
        keywords_entry = Entry(win, width=40)
        keywords_entry.pack()
        Label(win, text="Caminho (programa) ou URL (site):", fg="white", bg="#1b1d1f").pack(pady=(8, 2))
        path_entry = Entry(win, width=40)
        path_entry.pack()
        Button(win, text="Selecionar arquivo", command=lambda: path_entry.insert(0, filedialog.askopenfilename())).pack(pady=4)

        def save_command():
            cmd_data = {
                "type": cmd_type.get(),
                "name": name_entry.get(),
                "keywords": [k.strip().lower() for k in keywords_entry.get().split(",")],
            }
            if cmd_type.get() == "internal":
                cmd_data["path"] = path_entry.get()
            else:
                cmd_data["url"] = path_entry.get()

            try:
                with open("commands.json", "r+", encoding="utf-8") as f:
                    data = json.load(f)
                    data["commands"].append(cmd_data)
                    f.seek(0)
                    json.dump(data, f, indent=4, ensure_ascii=False)
                engine.load_custom_commands()
                messagebox.showinfo("Sucesso", "✅ Comando salvo com sucesso!")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar comando: {e}")

        Button(win, text="Salvar", command=save_command).pack(pady=10)

<<<<<<< HEAD
    def update_context_label(self):
        ctx = engine.context
        if ctx:
            self.context_label.configure(text=f"Contexto: 🟢 Dentro do {ctx.capitalize()}")
        else:
            self.context_label.configure(text="Contexto: —")
=======
>>>>>>> 1af2b3e86c591ccdca5a294d90673f0f6d8aee4c

# ---------------------------
# Tray Icon
# ---------------------------
def create_tray(app):
    def on_show(icon, item): app.deiconify()
    def on_quit(icon, item):
        icon.stop()
        try: app.destroy()
        except: pass

    image = Image.new("RGB", (64, 64), (0, 153, 255))
    menu = Menu(MenuItem("Mostrar Lynx", on_show), MenuItem("Sair", on_quit))
    icon = Icon("Lynx", image, "Lynx Assistant", menu)
    icon.run()

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    app = LynxApp()
    tray_thread = threading.Thread(target=create_tray, args=(app,), daemon=True)
    tray_thread.start()
    app.mainloop()
