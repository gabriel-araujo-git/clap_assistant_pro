import json
import os
import subprocess
import webbrowser
import platform
from pathlib import Path


class CommandEngine:
    """
    CommandEngine 100% baseado em JSON:
    - commands_builtin.json  (comandos fixos)
    - commands.json          (comandos customizados)
    """

    def __init__(self,
                 builtin_path: str = "data/commands_builtin.json",
                 custom_path: str = "data/commands.json"):

        self.builtin_path = builtin_path
        self.custom_path = custom_path

        # lista única com todos os comandos (builtin + custom)
        self.commands = []

        self.load_builtin_commands()
        self.load_custom_commands()

        print(f"[Lynx] {len(self.commands)} comandos carregados.")

    # ------------------------------------------------------------
    # Carregamento de arquivos JSON
    # ------------------------------------------------------------

    def load_builtin_commands(self):
        """Carrega o arquivo commands_builtin.json"""
        if not os.path.exists(self.builtin_path):
            print(f"[Lynx] WARNING: Arquivo {self.builtin_path} não encontrado.")
            return

        try:
            with open(self.builtin_path, "r", encoding="utf8") as f:
                data = json.load(f)

            for cmd in data.get("builtin_commands", []):
                self.commands.append(cmd)

        except Exception as e:
            print(f"[Lynx] Erro lendo commands_builtin.json: {e}")

    def load_custom_commands(self):
        """Carrega comandos customizados do usuário."""
        if not os.path.exists(self.custom_path):
            print(f"[Lynx] Nenhum commands.json encontrado. Criando um novo.")
            with open(self.custom_path, "w", encoding="utf8") as f:
                json.dump({"custom_commands": []}, f, indent=4, ensure_ascii=False)
            return

        try:
            with open(self.custom_path, "r", encoding="utf8") as f:
                data = json.load(f)

            for cmd in data.get("custom_commands", []):
                self.commands.append(cmd)

        except Exception as e:
            print(f"[Lynx] Erro lendo commands.json: {e}")

    # ------------------------------------------------------------
    # Normalização do texto
    # ------------------------------------------------------------

    def normalize(self, text: str) -> str:
        """
        Normaliza texto para melhorar matching:
        - lower()
        - remove acentos
        - remove palavras inúteis
        """
        import unicodedata
        import re

        t = text.lower().strip()

        # remover acentos
        t = unicodedata.normalize("NFKD", t)
        t = t.encode("ascii", "ignore").decode()

        # remover "por favor", "por gentileza", "abre", etc
        t = re.sub(r"\b(abrir|abra|abre|por favor|pfv|por gentileza)\b", "", t)
        t = " ".join(t.split())
        return t

    # ------------------------------------------------------------
    # Execução principal
    # ------------------------------------------------------------

    def execute(self, text: str) -> str:
        """
        Faz match contra todos os comandos.
        Retorna uma string com a resposta da execução.
        """
        norm = self.normalize(text)

        # procurar keyword que esteja dentro do texto
        for cmd in self.commands:
            for kw in cmd.get("keywords", []):
                if kw.lower() in norm:
                    return self.run_command(cmd)

        return f"❌ Não encontrei um comando correspondente a: {text}"

    # ------------------------------------------------------------
    # Execução de um comando do JSON
    # ------------------------------------------------------------

    def run_command(self, cmd: dict) -> str:
        """
        Executa um comando baseado no JSON:
        - type=url → abre site
        - type=executable → executa um .exe, .lnk ou comando no PATH
        - type=system → reiniciar, desligar, bloquear, etc.
        """
        cmd_type = cmd.get("type")

        # ----------------------------
        # ABRIR SITES
        # ----------------------------
        if cmd_type == "external" or cmd_type == "url":
            url = cmd.get("url")
            if not url:
                return "❌ URL inválida no comando."
            webbrowser.open(url)
            return f"🌐 Abrindo {url}"

        # ----------------------------
        # EXECUTAR PROGRAMAS
        # ----------------------------
        if cmd_type == "executable":
            path = cmd.get("path")
            if not path:
                return "❌ Caminho inválido para executable."

            try:
                # Se começar com ~/ converte para path real
                if path.startswith("~/"):
                    path = str(Path.home() / path[2:])

                subprocess.Popen(path, shell=False)
                return f"⚙️ Executando: {path}"

            except FileNotFoundError:
                # tenta como comando shell
                try:
                    subprocess.Popen(path, shell=True)
                    return f"⚙️ Executando via shell: {path}"
                except Exception:
                    return f"❌ Não foi possível abrir: {path}"

            except Exception as e:
                return f"❌ Erro ao executar: {e}"

        # ----------------------------
        # COMANDOS DE SISTEMA
        # ----------------------------
        if cmd_type == "system":
            syscmd = cmd.get("cmd")

            if syscmd == "LOCK":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                return "🔒 Computador bloqueado."

            if syscmd == "RESTART":
                os.system("shutdown /r /t 0")
                return "🔁 Reiniciando o computador..."

            if syscmd == "SHUTDOWN":
                os.system("shutdown /s /t 0")
                return "⏻ Desligando o computador..."

            if syscmd == "SLEEP":
                os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")
                return "😴 Colocando o computador para dormir..."

            return "❌ Comando de sistema inválido."

        return "❌ Tipo de comando desconhecido."
