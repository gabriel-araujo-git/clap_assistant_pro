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
            # Redes sociais
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

            # Streaming e música
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

            # Produtividade e trabalho
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

            # Bancos e pagamentos
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

            # Estudos e pesquisa
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

        # título
        self.label_title = ctk.CTkLabel(self, text="Lynx", font=ctk.CTkFont(size=18, weight="bold"), text_color="#2db7ff")
        self.label_title.pack(pady=(12, 6))

        # entrada
        self.input = ctk.CTkEntry(self, placeholder_text="Digite o comando (ex: 'ln teste', 'vscode')", width=320, height=36)
        self.input.pack(pady=(6, 8))
        self.input.bind("<Return>", self.on_enter)

        # resultado
        self.result = ctk.CTkLabel(self, text="", text_color="#d0d0d0", font=ctk.CTkFont(size=13))
        self.result.pack(pady=(2, 10))

        # botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=(0, 8))
        self.btn_close = ctk.CTkButton(btn_frame, text="Fechar", width=80, command=self.hide_window)
        self.btn_close.grid(row=0, column=0, padx=6)
        self.btn_help = ctk.CTkButton(btn_frame, text="Ajuda", width=80, command=self.show_help)
        self.btn_help.grid(row=0, column=1, padx=6)
        self.btn_add = ctk.CTkButton(btn_frame, text="Adicionar", width=80, command=self.show_add_command)
        self.btn_add.grid(row=0, column=2, padx=6)

        self.protocol("WM_DELETE_WINDOW", self.hide_window)

    def on_enter(self, event=None):
        cmd = self.input.get().strip()
        if not cmd:
            return
        result = engine.execute(cmd)
        self.result.configure(text=result)
        self.input.delete(0, "end")

    def hide_window(self):
        self.withdraw()

    def show_help(self):
        from tkinter import Toplevel, Label
        h = Toplevel(self)
        h.title("Lynx - Comandos rápidos")
        h.geometry("420x260")
        h.attributes("-topmost", True)
        txt = (
            "Comandos padrão (exemplos):\n\n"
            "- vscode / code / vs\n"
            "- ln / lnstudio / aln\n"
            "- ln teste / alnteste\n"
            "- ln prd / alnprd\n"
            "- youtube / github / google\n"
            "- explorer / notepad\n\n"
            "💡 Você pode adicionar novos comandos pelo botão 'Adicionar'."
        )
        Label(h, text=txt, justify="left", padx=12, pady=12).pack()

    def show_add_command(self):
        from tkinter import Toplevel, Label, Entry, Button, Radiobutton, StringVar

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
