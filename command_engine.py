import subprocess, webbrowser, os

class CommandEngine:
    def __init__(self):
        # Dicionário base com múltiplos sinônimos
        self.commands = {
            # VSCode
            ("abrir vscode", "vscode", "code", "vs"): self.open_vscode,

            # LN Studio
            ("abrir ln", "ln", "studio ln", "lnstudio", "aln", "lnstd", "std"): self.open_ln,

            # LN Teste
            ("abrir ln teste", "ln teste", "alnteste", "teste ln", "lntst", "tst"): self.open_ln_tst,

            # LN Produção
            ("abrir ln prd", "ln prd", "alnprd", "lnprod", "ln produção", "prd ln"): self.open_ln_prd,

            # Navegador / Chrome
            ("abrir navegador", "abrir chrome", "navegador", "chrome", "abrir web"): self.open_browser,
        }

    def execute(self, text: str):
        text = text.lower().strip()

        for keys, func in self.commands.items():
            for key in keys:
                if key in text:
                    return func()

        return f"Comando não reconhecido: {text}"

    # --- Ações principais ---
    def open_vscode(self):
        try:
            subprocess.Popen("code")
        except FileNotFoundError:
            subprocess.Popen(
                r"C:\Users\107457\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code\Visual Studio Code.lnk",
                shell=True
            )
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
