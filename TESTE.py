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
