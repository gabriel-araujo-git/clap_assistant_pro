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

        # comandos gerais e contextuais
        self.register_default_commands()
        self.register_context_actions()

        # carrega comandos personalizados (mantém compatibilidade)
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

        # atualiza indicador ao iniciar
        self.update_context_label()

    def on_enter(self, event=None):
        cmd = self.input.get().strip()
        if not cmd:
            return
        result = engine.execute(cmd)
        # se o engine mudou o contexto, atualizar o label
        self.update_context_label()
        self.result.configure(text=result)
        self.input.delete(0, "end")

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

    def update_context_label(self):
        ctx = engine.context
        if ctx:
            self.context_label.configure(text=f"Contexto: 🟢 Dentro do {ctx.capitalize()}")
        else:
            self.context_label.configure(text="Contexto: —")

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
