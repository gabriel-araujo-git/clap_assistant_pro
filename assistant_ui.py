# assistant_ui.py
import customtkinter as ctk
import threading
import subprocess
import webbrowser
import os
import json
from pystray import Icon, MenuItem, Menu
from PIL import Image
from tkinter import filedialog, messagebox
from tkinter import Toplevel, Text, Scrollbar, END, RIGHT, Y, LEFT, BOTH, Frame
from tkinter import Toplevel, Label, Entry, Button, Radiobutton, StringVar, filedialog, messagebox

# ---------------------------
# CommandEngine
# ---------------------------
class CommandEngine:
    def __init__(self):
        self.commands = {
            ("abrir vscode", "vscode", "code", "vs", "abrir code", "abrir vs", "open vscode"): self.open_vscode,
            ("abrir ln", "ln", "lnstudio", "studio ln", "aln", "lnstd", "std", "abrir ln studio"): self.open_ln,
            ("abrir ln teste", "ln teste", "alnteste", "teste ln", "lntst", "ln tst", "ln-test", "TST", "tst"): self.open_ln_tst,
            ("abrir ln prd", "ln prd", "alnprd", "lnprod", "ln produção", "prd ln", "ln-prd", "PRD", "prd"): self.open_ln_prd,
            ("abrir navegador", "abrir chrome", "navegador", "chrome", "abrir web", "open browser", "browser", "web"): self.open_browser,
            ("abrir explorer", "explorer", "explorar", "abrir explorador", "abrir explorador de arquivos"): self.open_explorer,
            ("bloco de notas", "notepad", "abrir notepad", "abrir bloco de notas"): self.open_notepad,
        }

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
            ("abrir outlook", "outlook", "email"): lambda: self.open_site("https://www.outlook.com"),
            

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
        self.load_custom_commands()

    def load_custom_commands(self):
        """Carrega comandos salvos pelo usuário (commands.json)"""
        try:
            with open("commands.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            for cmd in data.get("commands", []):
                if cmd["type"] == "internal":
                    func = lambda path=cmd["path"]: subprocess.Popen(path, shell=True)
                elif cmd["type"] == "external":
                    func = lambda url=cmd["url"]: webbrowser.open(url)
                else:
                    continue
                self.commands[tuple(cmd["keywords"])] = func
        except FileNotFoundError:
            with open("commands.json", "w", encoding="utf-8") as f:
                json.dump({"commands": []}, f, indent=4, ensure_ascii=False)

    def normalize(self, text: str) -> str:
        t = text.lower().strip()
        replacements = ["abrir o ", "abrir a ", "abrir ", "entrar em ", "entrar no ", "por favor ", "por favor, "]
        for r in replacements:
            t = t.replace(r, "")
        return " ".join(t.split())

    def execute(self, text: str) -> str:
        text = self.normalize(text)
        for keys, func in self.commands.items():
            for key in keys:
                if key in text:
                    try:
                        func()
                        return f"✅ Executando: {key}"
                    except Exception as e:
                        return f"❌ Erro ao executar: {e}"
        return f"❓ Comando não reconhecido: '{text}'"

    # ---------------------------
    # Funções padrão
    # ---------------------------
    def open_vscode(self) -> str:
        try:
            subprocess.Popen("code", shell=True)
            return "🚀 Abrindo VSCode..."
        except Exception:
            possible = [
                r"C:\Users\107457\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk",
                r"C:\Program Files\Microsoft VS Code\Code.exe",
                r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
            ]
            for p in possible:
                if os.path.exists(p):
                    subprocess.Popen(p, shell=True)
                    return "🚀 Abrindo VSCode (fallback)..."
            return "❌ VSCode não encontrado."

    def open_ln(self): subprocess.Popen(r"C:\LnStudio\eclipse.exe", shell=True)
    def open_ln_tst(self): webbrowser.open("https://mingle-portal.inforcloudsuite.com/v2/ELETROFRIO_TST/e6d06856-3c6a-44d9-8ce3-ed3affd6ab21")
    def open_ln_prd(self): webbrowser.open("https://mingle-portal.inforcloudsuite.com/v2/ELETROFRIO_PRD/a8841f8a-7964-4977-b108-14edbb6ddb4f")
    def open_site(self, url): webbrowser.open(url)
    def open_browser(self): subprocess.Popen("chrome", shell=True)
    def open_explorer(self): subprocess.Popen("explorer", shell=True)
    def open_notepad(self): subprocess.Popen("notepad.exe", shell=True)

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
        self.geometry("360x200")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(fg_color="#0f1113")

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
    def on_enter(self, event=None):
        cmd = self.input.get().strip()
        if not cmd:
            return
        result = engine.execute(cmd)
        self.show_result_feedback(result)
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
        h = Toplevel(self)
        h.title("Lynx - Comandos e Dicas")
        h.geometry("560x420")
        h.configure(bg="#1b1d1f")
        h.attributes("-topmost", True)

        # ---------------------------
        # Container com Scroll
        # ---------------------------
        container = Frame(h, bg="#1b1d1f")
        container.pack(fill=BOTH, expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(container)
        scrollbar.pack(side=RIGHT, fill=Y)

        text_box = Text(
            container,
            wrap="word",
            bg="#1b1d1f",
            fg="#d0d0d0",
            insertbackground="white",
            font=("Consolas", 11),
            yscrollcommand=scrollbar.set,
            relief="flat",
            padx=14,
            pady=10,
        )
        text_box.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=text_box.yview)

        # ---------------------------
        # Função auxiliar para escrever seções
        # ---------------------------
        def add_section(title, emoji, commands, color="#2db7ff"):
            text_box.insert(END, f"\n{emoji} ", ("emoji",))
            text_box.insert(END, f"{title}\n", ("section_title",))
            for keys in commands:
                sample = ", ".join(keys[:3])
                text_box.insert(END, f"   • {sample}\n", ("command",))

        # ---------------------------
        # Separar comandos por categoria
        # ---------------------------
        system_cmds, site_cmds, app_cmds, custom_cmds = [], [], [], []

        for keys, func in engine.commands.items():
            first = next(iter(keys))
            if "http" in str(func):  # sites externos
                site_cmds.append(keys)
            elif any(x in first for x in ("explorer", "notepad", "cmd", "calc", "taskmgr", "shutdown", "reiniciar")):
                system_cmds.append(keys)
            elif any(x in first for x in ("ln", "vscode", "studio", "prd", "teste")):
                app_cmds.append(keys)
            else:
                custom_cmds.append(keys)

        # ---------------------------
        # Título
        # ---------------------------
        text_box.insert(END, "⚡ LYNX - GUIA DE COMANDOS RÁPIDOS ⚡\n", ("title",))
        

        # ---------------------------
        # Seções principais
        # ---------------------------
        if app_cmds: add_section("Programas / Ambientes", "💻", app_cmds, "#2db7ff")
        if site_cmds: add_section("Sites e Ferramentas Online", "🌐", site_cmds, "#00c896")
        if system_cmds: add_section("Comandos do Sistema", "⚙️", system_cmds, "#ffaa00")
        if custom_cmds: add_section("Comandos Personalizados", "🧠", custom_cmds, "#ff66cc")

        # ---------------------------
        # Dicas e atalhos
        # ---------------------------
        text_box.insert(END, "\n💡 DICAS ÚTEIS:\n", ("section_title",))
        text_box.insert(END, " - Use sinônimos como 'abrir', 'entrar em', etc.\n")
        text_box.insert(END, " - Adicione novos comandos no botão 'Adicionar'.\n")
        text_box.insert(END, " - O Lynx reconhece tanto programas quanto sites.\n")
        text_box.insert(END, " - Os comandos são salvos em 'commands.json'.\n\n")

        text_box.insert(END, "⌨️ ATALHOS:\n", ("section_title",))
        text_box.insert(END, " - ENTER → Executar comando\n")
        text_box.insert(END, " - ESC → Fechar janela\n")

        # ---------------------------
        # Estilos de texto
        # ---------------------------
        text_box.tag_configure("title", foreground="#2db7ff", font=("Consolas", 13, "bold"))
        text_box.tag_configure("section_title", foreground="#00b4ff", font=("Consolas", 12, "bold"))
        text_box.tag_configure("command", foreground="#d0d0d0", font=("Consolas", 10))
        text_box.tag_configure("emoji", font=("Consolas", 12))
        text_box.config(state="disabled")

        # ---------------------------
        # Botão inferior
        # ---------------------------
        def open_json():
            path = os.path.abspath("commands.json")
            if os.path.exists(path):
                os.startfile(path)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump({"commands": []}, f, indent=4, ensure_ascii=False)
                os.startfile(path)

        btn = ctk.CTkButton(h, text="Abrir commands.json", command=open_json, width=220)
        btn.pack(pady=10)


    def show_add_command(self):
        from tkinter import Toplevel, Label, Entry, Button, Radiobutton, StringVar, filedialog, messagebox

        win = Toplevel(self)
        win.title("Adicionar Comando")
        win.geometry("380x360")
        win.configure(bg="#1b1d1f")
        win.attributes("-topmost", True)

        Label(win, text="Tipo de comando:", fg="white", bg="#1b1d1f").pack(pady=4)

        # O segredo: vincular o StringVar ao Toplevel
        win.cmd_type = StringVar(win, value="internal")

        rb_frame = Frame(win, bg="#1b1d1f")
        rb_frame.pack()
        Radiobutton(rb_frame, text="Interno (programa)", variable=win.cmd_type,
                    value="internal", bg="#1b1d1f", fg="white", selectcolor="#2b2d2f").pack(side="left", padx=10)
        Radiobutton(rb_frame, text="Externo (site)", variable=win.cmd_type,
                    value="external", bg="#1b1d1f", fg="white", selectcolor="#2b2d2f").pack(side="left", padx=10)

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
            cmd_type = win.cmd_type.get()  # sempre seguro agora
            name = name_entry.get().strip()
            keywords = [k.strip().lower() for k in keywords_entry.get().split(",") if k.strip()]
            path = path_entry.get().strip()

            if not name or not keywords or not path:
                messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos antes de salvar.")
                return

            cmd_data = {"type": cmd_type, "name": name, "keywords": keywords}
            if cmd_type == "internal":
                cmd_data["path"] = path
            else:
                cmd_data["url"] = path

            try:
                # Garante arquivo válido
                if not os.path.exists("commands.json"):
                    with open("commands.json", "w", encoding="utf-8") as f:
                        json.dump({"commands": []}, f, indent=4, ensure_ascii=False)

                with open("commands.json", "r+", encoding="utf-8") as f:
                    try:
                        data = json.load(f)
                    except json.JSONDecodeError:
                        data = {"commands": []}

                    data["commands"].append(cmd_data)
                    f.seek(0)
                    json.dump(data, f, indent=4, ensure_ascii=False)
                    f.truncate()

                engine.commands.clear()
                engine.__init__()

                messagebox.showinfo("Sucesso", f"Comando '{name}' salvo com sucesso!")
                win.destroy()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar comando:\n{e}")

        Button(win, text="Salvar", command=save_command).pack(pady=10)




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