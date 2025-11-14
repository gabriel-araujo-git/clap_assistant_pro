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
import customtkinter as ctk
from tkinter import filedialog, messagebox, Frame, Label
import os
import json
import subprocess
import webbrowser
from urllib.parse import urlparse
from PIL import Image, ImageTk

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
    def add_custom_command(self, cmd_data):
        """Adiciona e salva um comando personalizado dinamicamente."""
        # Garante arquivo
        if not os.path.exists("commands.json"):
            with open("commands.json", "w", encoding="utf-8") as f:
                json.dump({"commands": []}, f, indent=4, ensure_ascii=False)

        # Salva no JSON
        with open("commands.json", "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"commands": []}

            data["commands"].append(cmd_data)
            f.seek(0)
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.truncate()

        # Adiciona na memória
        if cmd_data["type"] == "internal":
            func = lambda path=cmd_data["path"]: subprocess.Popen(path, shell=True)
        else:
            func = lambda url=cmd_data["url"]: webbrowser.open(url)
        self.commands[tuple(cmd_data["keywords"])] = func

    
    
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
            text_color="#05a4fa"
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
        self.btn_help = ctk.CTkButton(btn_frame, text="ⓘ Ajuda", width=80, command=self.show_help)
        self.btn_help.grid(row=0, column=1, padx=6)
        self.btn_add = ctk.CTkButton(btn_frame, text="➕Adicionar Comando", width=80, command=self.show_add_command)
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
        self.quit()
        os._exit(0)


    def show_help(self):
        

        # ---------------------------
        # Janela principal
        # ---------------------------
        h = ctk.CTkToplevel(self)
        h.title("Lynx — Ajuda e Comandos")
        h.geometry("650x540")
        h.attributes("-topmost", True)
        h.configure(fg_color="#101214")


        # ---------------------------
        # Barra de busca
        # ---------------------------
        search_frame = ctk.CTkFrame(h, fg_color="#15171a", corner_radius=10)
        search_frame.pack(fill="x", padx=12, pady=(12, 6))


        search_entry = ctk.CTkEntry(
        search_frame,
        placeholder_text="Buscar comando, alias ou descrição...",
        height=36,
        corner_radius=10
        )
        search_entry.pack(fill="x", padx=12, pady=12)


        # ---------------------------
        # Área scrollável
        # ---------------------------
        scroll_frame = ctk.CTkScrollableFrame(h, fg_color="#15171a", corner_radius=12)
        scroll_frame.pack(fill="both", expand=True, padx=12, pady=6)


        # ---------------------------
        # Transformar os comandos do engine para exibição
        # ---------------------------
        command_cards = []


        for keys, func in engine.commands.items():
            main_cmd = list(keys)[0]
            aliases = ", ".join(keys[1:]) if len(keys) > 1 else "—"


            if "http" in str(func) or "open_site" in str(func):
                action = "Abre um site"
            elif "subprocess" in func.__code__.co_names:
                action = "Executa um programa"
            else:
                action = "Ação interna"


            card = ctk.CTkFrame(scroll_frame, fg_color="#1b1e21", corner_radius=10)
            card.pack(fill="x", padx=8, pady=6)


            lbl_cmd = ctk.CTkLabel(
            card,
            text=main_cmd,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#00b4ff"
            )
            lbl_cmd.pack(anchor="w", padx=12, pady=(10, 2))


            lbl_alias = ctk.CTkLabel(
            card,
            text=f"Aliases: {aliases}",
            font=ctk.CTkFont(size=12),
            text_color="#a8b3bd"
            )
            lbl_alias.pack(anchor="w", padx=12)


            lbl_action = ctk.CTkLabel(
            card,
            text=f"Ação: {action}",
            font=ctk.CTkFont(size=12),
            text_color="#d0d0d0"
            )
            lbl_action.pack(anchor="w", padx=12, pady=(0, 10))


            command_cards.append((card, main_cmd, aliases, action))


        # ---------------------------
        # Função de filtro
        # ---------------------------
        def apply_filter(event=None):
            text = search_entry.get().lower().strip()
            for card, cmd, alias, action in command_cards:
                data = f"{cmd} {alias} {action}".lower()
                card.pack_forget()
                if text in data:
                    card.pack(fill="x", padx=8, pady=6)


        search_entry.bind("<KeyRelease>", apply_filter)



    def show_add_command(self):
       

        # Helpers
        def is_url(s: str):
            try:
                p = urlparse(s)
                return p.scheme in ("http", "https") and p.netloc != ""
            except Exception:
                return False

        def file_exists(s: str):
            return os.path.exists(s) and os.path.isfile(s)

        def guess_type_from_path(s: str):
            if is_url(s):
                return "external"
            if file_exists(s):
                return "internal"
            return None

        def load_commands_json():
            if not os.path.exists("commands.json"):
                with open("commands.json", "w", encoding="utf-8") as f:
                    json.dump({"commands": [], "recent": []}, f, indent=4, ensure_ascii=False)
            with open("commands.json", "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {"commands": [], "recent": []}

        def save_commands_json(data):
            with open("commands.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        def add_recent(name):
            data = load_commands_json()
            rec = data.get("recent", [])
            if name in rec:
                rec.remove(name)
            rec.insert(0, name)
            data["recent"] = rec[:6]
            save_commands_json(data)

        # Build window
        win = ctk.CTkToplevel(self)
        win.title("Adicionar Comando — Lynx")
        win.geometry("640x520")
        win.transient(self)
        win.attributes("-topmost", True)
        win.configure(fg_color="#0f1113")

        # Header
        header = ctk.CTkFrame(win, fg_color="transparent")
        header.pack(fill="x", padx=12, pady=(12, 6))
        lbl_title = ctk.CTkLabel(header, text="Adicionar Comando", font=ctk.CTkFont(size=16, weight="bold"), text_color="#05a4fa")
        lbl_title.pack(side="left")

        # Mode toggle
        mode_var = ctk.StringVar(value="simple")
        def set_mode(m):
            mode_var.set(m)
            if m == "simple":
                advanced_frame.pack_forget()
                simple_frame.pack(fill="x", padx=12, pady=(8, 6))
            else:
                simple_frame.pack_forget()
                advanced_frame.pack(fill="x", padx=12, pady=(8, 6))
        mode_switch = ctk.CTkSegmentedButton(header, values=["simple", "advanced"], command=set_mode)
        mode_switch.set("simple")
        mode_switch.pack(side="right")

        # Main area
        content = ctk.CTkFrame(win, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # ---------- Simple frame ----------
        simple_frame = ctk.CTkFrame(content, fg_color="#101214", corner_radius=8)
        simple_frame.pack(fill="x", pady=(8, 6))

        lbl_name = ctk.CTkLabel(simple_frame, text="Nome do comando", anchor="w")
        lbl_name.pack(fill="x", padx=12, pady=(10, 2))
        entry_name = ctk.CTkEntry(simple_frame)
        entry_name.pack(fill="x", padx=12)

        lbl_keywords = ctk.CTkLabel(simple_frame, text="Palavras-chave (digite e pressione Enter)", anchor="w")
        lbl_keywords.pack(fill="x", padx=12, pady=(8, 2))

        chips_frame = ctk.CTkFrame(simple_frame, fg_color="transparent")
        chips_frame.pack(fill="x", padx=12, pady=(0, 6))

        keyword_var = ctk.StringVar()
        entry_kw = ctk.CTkEntry(simple_frame, textvariable=keyword_var)
        entry_kw.pack(fill="x", padx=12, pady=(0, 6))

        # chips storage
        chips = []

        def redraw_chips():
            for w in chips_frame.winfo_children():
                w.destroy()
            for k in chips:
                chip_wrap = Frame(chips_frame, bg="#101217")
                chip_wrap.pack(side="left", padx=6, pady=6)
                lbl = Label(chip_wrap, text=k, bg="#101217", fg="#cbd5db", padx=8, pady=4)
                lbl.pack(side="left")
                btn = ctk.CTkButton(chip_wrap, text="x", width=26, height=22,
                                    command=lambda key=k: remove_chip(key), corner_radius=8)
                btn.pack(side="left", padx=(6,0))

        def add_chip_from_entry(event=None):
            v = entry_kw.get().strip().lower()
            if not v:
                return
            parts = [p.strip() for p in v.replace(";",",").split(",") if p.strip()]
            changed = False
            for p in parts:
                if p and p not in chips:
                    chips.append(p)
                    changed = True
            if changed:
                redraw_chips()
            entry_kw.delete(0, "end")

        def remove_chip(key):
            if key in chips:
                chips.remove(key)
                redraw_chips()

        entry_kw.bind("<Return>", add_chip_from_entry)

        lbl_path = ctk.CTkLabel(simple_frame, text="Caminho do programa ou URL", anchor="w")
        lbl_path.pack(fill="x", padx=12, pady=(8, 2))
        entry_path = ctk.CTkEntry(simple_frame)
        entry_path.pack(fill="x", padx=12)

        # small controls row
        controls_row = ctk.CTkFrame(simple_frame, fg_color="transparent")
        controls_row.pack(fill="x", padx=12, pady=(8, 12))

        def pick_file():
            p = filedialog.askopenfilename(title="Selecione o executável ou arquivo")
            if p:
                entry_path.delete(0, "end")
                entry_path.insert(0, p)
                detect_type_and_icon()

        def pick_icon():
            p = filedialog.askopenfilename(title="Selecione um ícone ou imagem (png, ico, jpg)", filetypes=[("Images","*.png;*.ico;*.jpg;*.jpeg")])
            if p:
                load_icon_preview(p)
                win.selected_icon = p

        btn_file = ctk.CTkButton(controls_row, text="Selecionar arquivo", width=160, command=pick_file)
        btn_file.pack(side="left")

        btn_icon = ctk.CTkButton(controls_row, text="Selecionar ícone", width=140, command=pick_icon)
        btn_icon.pack(side="left", padx=(8,0))

        # Type hint label
        type_hint = ctk.CTkLabel(simple_frame, text="Tipo: —", anchor="w", text_color="#a0a9ad")
        type_hint.pack(fill="x", padx=12, pady=(0,6))

        # Preview area
        preview_card = ctk.CTkFrame(simple_frame, fg_color="#0f1416", corner_radius=8)
        preview_card.pack(fill="x", padx=12, pady=(6, 12))
        preview_lbl = ctk.CTkLabel(preview_card, text="Preview: (preencha os campos)", anchor="w")
        preview_lbl.pack(fill="x", padx=10, pady=8)

        # History
        history_card = ctk.CTkFrame(simple_frame, fg_color="transparent")
        history_card.pack(fill="x", padx=12, pady=(0,12))
        hist_lbl = ctk.CTkLabel(history_card, text="Últimos comandos (recentes):", anchor="w", text_color="#9aa4ad")
        hist_lbl.pack(anchor="w")
        hist_frame = ctk.CTkFrame(history_card, fg_color="transparent")
        hist_frame.pack(fill="x", pady=(6,0))

        def load_recent():
            data = load_commands_json()
            for w in hist_frame.winfo_children():
                w.destroy()
            for name in data.get("recent", [])[:6]:
                b = ctk.CTkButton(hist_frame, text=name, width=120, command=lambda n=name: fill_from_recent(n))
                b.pack(side="left", padx=6)

        def fill_from_recent(name):
            data = load_commands_json()
            for c in data.get("commands", []):
                if c.get("name") == name:
                    entry_name.delete(0,"end"); entry_name.insert(0, c.get("name",""))
                    chips.clear()
                    for k in c.get("keywords", []):
                        chips.append(k)
                    redraw_chips()
                    if c.get("type") == "internal":
                        entry_path.delete(0,"end"); entry_path.insert(0, c.get("path",""))
                    else:
                        entry_path.delete(0,"end"); entry_path.insert(0, c.get("url",""))
                    detect_type_and_icon()
                    break

        load_recent()

        # ---------- Advanced frame ----------
        advanced_frame = ctk.CTkFrame(content, fg_color="#101214", corner_radius=8)
        # advanced fields (hidden by default)
        adv_lbl = ctk.CTkLabel(advanced_frame, text="Modo Avançado — Campos extras", anchor="w")
        adv_lbl.pack(fill="x", padx=12, pady=(8,2))
        lbl_desc = ctk.CTkLabel(advanced_frame, text="Descrição (opcional)", anchor="w")
        lbl_desc.pack(fill="x", padx=12, pady=(6,2))
        entry_desc = ctk.CTkEntry(advanced_frame)
        entry_desc.pack(fill="x", padx=12, pady=(0,8))

        lbl_category = ctk.CTkLabel(advanced_frame, text="Categoria (opcional)", anchor="w")
        lbl_category.pack(fill="x", padx=12, pady=(6,2))
        category_var = ctk.StringVar(value="other")
        category_entry = ctk.CTkEntry(advanced_frame, textvariable=category_var)
        category_entry.pack(fill="x", padx=12, pady=(0,8))

        # Icon preview area
        icon_preview_frame = ctk.CTkFrame(content, fg_color="transparent")
        icon_preview_frame.pack(fill="x", padx=12, pady=(0,6))
        icon_label = ctk.CTkLabel(icon_preview_frame, text="Ícone: (nenhum)", anchor="w", text_color="#9aa4ad")
        icon_label.pack(side="left")
        icon_canvas_holder = ctk.CTkFrame(icon_preview_frame, fg_color="transparent")
        icon_canvas_holder.pack(side="right")
        icon_img_label = None
        win.selected_icon = None

        def load_icon_preview(path):
            nonlocal icon_img_label
            try:
                img = Image.open(path)
                img.thumbnail((48,48))
                tkimg = ImageTk.PhotoImage(img)
                # destroy old
                for w in icon_canvas_holder.winfo_children():
                    w.destroy()
                l = ctk.CTkLabel(icon_canvas_holder, image=tkimg, text="")
                l.image = tkimg
                l.pack()
                icon_label.configure(text=f"Ícone: {os.path.basename(path)}")
                win.selected_icon = path
            except Exception:
                icon_label.configure(text="Ícone: (falha ao carregar)")

        def detect_type_and_icon(event=None):
            p = entry_path.get().strip()
            t = guess_type_from_path(p)
            if t == "external":
                type_hint.configure(text="Tipo: Externo (URL)", text_color="#7bd389")
                category_var.set("web")
            elif t == "internal":
                type_hint.configure(text="Tipo: Interno (programa)", text_color="#7bd389")
                category_var.set("local")
                # Try to find icon in same folder
                try:
                    folder = os.path.dirname(p)
                    base = os.path.splitext(os.path.basename(p))[0]
                    for ext in (".ico", ".png", ".jpg", ".jpeg"):
                        candidate = os.path.join(folder, base + ext)
                        if os.path.exists(candidate):
                            load_icon_preview(candidate)
                            break
                except Exception:
                    pass
            else:
                type_hint.configure(text="Tipo: Não detectado", text_color="#d1a3a3")
            # update preview
            update_preview()

        entry_path.bind("<FocusOut>", detect_type_and_icon)
        entry_path.bind("<Return>", detect_type_and_icon)

        def update_preview():
            name = entry_name.get().strip()
            ks = ", ".join(chips) if chips else "(nenhuma keyword)"
            path = entry_path.get().strip()
            desc = entry_desc.get().strip() if 'entry_desc' in locals() else ""
            t = "URL" if is_url(path) else ("Arquivo" if file_exists(path) else "(não válido)")
            preview_lbl.configure(text=f"Preview:\n- Nome: {name or '(não definido)'}\n- Keywords: {ks}\n- Target: {t}\n- Descrição: {desc or '(sem descrição)'}")

        entry_name.bind("<KeyRelease>", lambda e: update_preview())
        entry_kw.bind("<KeyRelease>", lambda e: None)  # handled by Enter
        entry_path.bind("<KeyRelease>", lambda e: update_preview())
        entry_desc.bind("<KeyRelease>", lambda e: update_preview)

        # Test and Save buttons
        actions_row = ctk.CTkFrame(content, fg_color="transparent")
        actions_row.pack(fill="x", padx=12, pady=(6,12))

        status_label = ctk.CTkLabel(actions_row, text="", anchor="w", text_color="#a8b3bd")
        status_label.pack(side="left")

        def set_status(text, ok=True):
            status_label.configure(text=text, text_color="#7bd389" if ok else "#ff7373")
            # clear after 3s
            win.after(3000, lambda: status_label.configure(text=""))

        def test_command():
            target = entry_path.get().strip()
            if is_url(target):
                try:
                    webbrowser.open(target)
                    set_status("URL aberta (teste).", ok=True)
                except Exception as e:
                    set_status(f"Erro ao abrir URL: {e}", ok=False)
            elif file_exists(target):
                try:
                    subprocess.Popen(target, shell=True)
                    set_status("Programa iniciado (teste).", ok=True)
                except Exception as e:
                    set_status(f"Erro ao executar: {e}", ok=False)
            else:
                set_status("Target inválido para teste.", ok=False)

        btn_test = ctk.CTkButton(actions_row, text="Testar", width=120, command=test_command)
        btn_test.pack(side="right", padx=(6,0))

        def validate_all():
            name = entry_name.get().strip()
            if not name:
                return False, "Nome obrigatório."
            if any(c.get("name") == name for c in load_commands_json().get("commands", [])):
                return False, "Já existe um comando com esse nome."
            if not chips:
                return False, "Adicione ao menos uma palavra-chave."
            targ = entry_path.get().strip()
            if not targ:
                return False, "Informe caminho ou URL."
            if not (is_url(targ) or file_exists(targ)):
                return False, "Caminho/URL inválido ou não encontrado."
            return True, ""

        def save_command():
            ok, msg = validate_all()
            if not ok:
                set_status(msg, ok=False)
                return
            name = entry_name.get().strip()
            targ = entry_path.get().strip()
            cmd_type = "external" if is_url(targ) else "internal"
            cmd_data = {"type": cmd_type, "name": name, "keywords": chips.copy()}
            if cmd_type == "internal":
                cmd_data["path"] = targ
            else:
                cmd_data["url"] = targ
            desc = entry_desc.get().strip() if 'entry_desc' in locals() else ""
            if desc:
                cmd_data["description"] = desc
            if win.selected_icon:
                cmd_data["icon"] = win.selected_icon
            # write
            data = load_commands_json()
            data.setdefault("commands", []).append(cmd_data)
            save_commands_json(data)
            add_recent(name)
            load_recent()
            set_status("Comando salvo com sucesso.", ok=True)
            # add to engine in runtime
            try:
                if cmd_type == "internal":
                    func = lambda path=targ: subprocess.Popen(path, shell=True)
                else:
                    func = lambda url=targ: webbrowser.open(url)
                engine.commands[tuple(cmd_data["keywords"])] = func
            except Exception:
                pass
            win.after(400, win.focus_force)
            win.after(800, win.destroy)

        btn_save = ctk.CTkButton(actions_row, text="Salvar", width=120, command=save_command)
        btn_save.pack(side="right", padx=(6,0))

        # initial UI state
        set_mode("simple")
        redraw_chips()
        update_preview()
        detect_type_and_icon()

# ---------------------------
# Tray Icon
# ---------------------------
def create_tray(app):
    def on_show(icon, item):
        app.deiconify()

    def on_quit(icon, item):
        try:
            icon.stop()  # para o tray loop
            app.quit()   # encerra o mainloop do Tkinter
            os._exit(0)  # força término completo do processo
        except Exception:
            os._exit(0)

    image = Image.new("RGB", (64, 64), (0, 153, 255))
    menu = Menu(
        MenuItem("Mostrar Lynx", on_show),
        MenuItem("Sair", on_quit)
    )
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
