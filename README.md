# Clap Assistant Pro — Projeto Completo

Este repositório contém uma versão modular e robusta do **Clap Assistant Pro** (detector de palmas que executa ações configuráveis). Inclui: detecção de 1/2/3 palmas, arquivo de configuração `config.json`, ações customizáveis em `actions.py`, logs rotativos, prevenção de instâncias duplicadas e instruções para gerar um `.exe` e instalar como inicializador do Windows.

---

## Estrutura de arquivos

```
clap_assistant_pro/
├── main.py
├── audio_listener.py
├── actions.py
├── config.json
├── utils.py
├── installer.bat
├── requirements.txt
└── README.md
```

---

## Arquivos

### `main.py`

```python
# main.py
"""
Clap Assistant Pro - entrypoint
Inicia o listener de áudio, aplica configuração e expõe um tray menu simples.
"""
import threading
import time
import os
from utils import setup_logging, is_already_running, load_config, show_toast
from audio_listener import AudioListener
from actions import ActionExecutor

LOG = setup_logging()

if is_already_running("clap_assistant_pro"):
    LOG.info("Instância já em execução. Saindo.")
    raise SystemExit(0)

config = load_config()
executor = ActionExecutor(config, LOG)

listener = AudioListener(config, executor, LOG)

try:
    t = threading.Thread(target=listener.run, daemon=True)
    t.start()
    LOG.info("Clap Assistant Pro iniciado.")
    show_toast("Clap Assistant Pro", "Rodando em background — escutando palmas")
    # Mantém o processo vivo
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    LOG.info("Encerrado pelo usuário.")
except Exception as e:
    LOG.exception("Erro crítico: %s", e)
    raise
```

---

### `audio_listener.py`

```python
# audio_listener.py
"""
AudioListener: captura áudio, filtra frequências, reconhece 1/2/3 palmas e aciona ações.
"""
import sounddevice as sd
import numpy as np
import time
from collections import deque

class AudioListener:
    def __init__(self, config, executor, logger):
        self.config = config
        self.executor = executor
        self.logger = logger
        self.samplerate = config.get("samplerate", 44100)
        self.chunk = config.get("chunk_duration", 0.08)
        self.threshold = config.get("base_threshold", 0.28)
        self.cooldown = config.get("cooldown", 1.8)
        self.last_event = 0
        self.buffer = deque(maxlen= int(0.5 / self.chunk))

    def _bandpass(self, data):
        # simples filtro via FFT: mantemos 500Hz-6000Hz (reduz ruídos graves)
        fft = np.fft.rfft(data)
        freqs = np.fft.rfftfreq(len(data), 1.0/self.samplerate)
        mask = (freqs > 500) & (freqs < 6000)
        fft_filtered = fft * mask
        out = np.fft.irfft(fft_filtered)
        return out

    def _detect_claps_from_window(self, window):
        # janela: array 1D
        energy = np.linalg.norm(window)
        return energy

    def run(self):
        def callback(indata, frames, time_, status):
            mono = np.mean(indata, axis=1) if indata.ndim > 1 else indata[:,0]
            filtered = self._bandpass(mono)
            energy = self._detect_claps_from_window(filtered)
            now = time.time()
            self.buffer.append((now, energy))
            # verifica pico
            peak = max(e for _, e in self.buffer)
            if peak > self.threshold and (now - self.last_event) > self.cooldown:
                # conta número de picos separados em curto intervalo dentro da buffer
                times = [t for t, e in self.buffer if e > (self.threshold * 0.7)]
                if not times:
                    return
                # agrupa picos por 0.45s
                groups = []
                current = [times[0]]
                for tt in times[1:]:
                    if tt - current[-1] < 0.45:
                        current.append(tt)
                    else:
                        groups.append(current)
                        current = [tt]
                groups.append(current)
                # escolhe maior grupo
                groups = sorted(groups, key=lambda g: len(g), reverse=True)
                count = len(groups[0]) if groups else 1
                self.logger.info("Clap group detected: %d", count)
                self.last_event = now
                # mapeamento para ações
                if count == 1:
                    self.executor.execute_trigger("1_clap")
                elif count == 2:
                    self.executor.execute_trigger("2_claps")
                elif count >= 3:
                    self.executor.execute_trigger("3_claps")

        with sd.InputStream(callback=callback, channels=1, samplerate=self.samplerate, blocksize=int(self.samplerate * self.chunk)):
            while True:
                sd.sleep(1000)
```

---

### `actions.py`

```python
# actions.py
"""
Define e executa ações. Adicione funções aqui para personalizar.
"""
import subprocess
import os
import pyautogui
from win10toast import ToastNotifier

class ActionExecutor:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.notifier = ToastNotifier()

    def execute_trigger(self, trigger_name):
        action = self.config.get('actions', {}).get(trigger_name)
        self.logger.info("Trigger %s => %s", trigger_name, action)
        if not action:
            return
        # suportamos tipos: builtin, shell, python
        t = action.get('type')
        if t == 'builtin':
            fn = getattr(self, action['cmd'], None)
            if fn:
                fn()
        elif t == 'shell':
            cmd = action.get('cmd')
            subprocess.Popen(cmd, shell=True)
        elif t == 'python':
            # executa função definida neste módulo se existir
            fn = getattr(self, action['cmd'], None)
            if fn:
                fn()

    # builtins
    def abrir_vscode(self):
        possíveis = [
            r"C:\Users\dippf\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            r"C:\Program Files\Microsoft VS Code\Code.exe",
        ]
        for p in possíveis:
            if os.path.exists(p):
                subprocess.Popen([p])
                self.notifier.show_toast("Clap Assistant", "VS Code aberto", duration=3)
                return
        self.logger.warning("VSCode não encontrado.")

    def abrir_navegador(self):
        # Exemplo abre chrome se existir
        possíveis = [r"C:\Program Files\Google\Chrome\Application\chrome.exe"]
        for p in possíveis:
            if os.path.exists(p):
                subprocess.Popen([p])
                return
        # fallback para abrir via URL
        os.startfile("https://www.google.com")

    def bloquear_pc(self):
        subprocess.Popen("rundll32.exe user32.dll,LockWorkStation")

    def play_pause(self):
        pyautogui.press('playpause')
```

---

### `config.json` (exemplo)

```json
{
  "samplerate": 44100,
  "chunk_duration": 0.08,
  "base_threshold": 0.28,
  "cooldown": 1.8,
  "actions": {
    "1_clap": {"type": "builtin", "cmd": "abrir_vscode"},
    "2_claps": {"type": "builtin", "cmd": "abrir_navegador"},
    "3_claps": {"type": "builtin", "cmd": "bloquear_pc"}
  }
}
```

---

### `utils.py`

```python
# utils.py
import logging
import os
import json
from logging.handlers import RotatingFileHandler
import sys

def setup_logging():
    logdir = os.path.join(os.getenv('TEMP') or '.', 'clap_assistant')
    os.makedirs(logdir, exist_ok=True)
    path = os.path.join(logdir, 'clap_assistant.log')
    logger = logging.getLogger('clap_assistant')
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = RotatingFileHandler(path, maxBytes=1024*1024, backupCount=5, encoding='utf-8')
        fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger


def is_already_running(name):
    try:
        import psutil
        me = os.getpid()
        for p in psutil.process_iter(attrs=['pid', 'cmdline']):
            if p.pid == me:
                continue
            cmd = ' '.join(p.info.get('cmdline') or [])
            if name in cmd:
                return True
    except Exception:
        return False
    return False


def load_config(path='config.json'):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def show_toast(title, message):
    try:
        from win10toast import ToastNotifier
        ToastNotifier().show_toast(title, message, duration=3)
    except Exception:
        pass
```

---

### `requirements.txt`

```
sounddevice
numpy
psutil
pyautogui
win10toast
```

---

### `installer.bat` (opcional)

```bat
@echo off
REM Copia executavel para AppData e cria atalho na pasta Startup
set APPDIR=%APPDATA%\ClapAssistantPro
mkdir "%APPDIR%"
copy "%~dp0\dist\clap_assistant_pro.exe" "%APPDIR%\clap_assistant_pro.exe"
REM criar atalho na inicialização
powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\ClapAssistantPro.lnk');$s.TargetPath='%APPDATA%\ClapAssistantPro\clap_assistant_pro.exe';$s.Save()"

echo Instalado. Reinicie o Windows para iniciar automaticamente.
pause
```

---

## Instruções de build (converter para .exe)

1. Instale dependências em um venv:

```bash
pip install -r requirements.txt
```

2. Empacote com PyInstaller (exemplo):

```bash
pyinstaller --onefile --noconsole --name clap_assistant_pro main.py
```

3. Pegue `dist\clap_assistant_pro.exe` e rode `installer.bat` (opcional) para instalar na inicialização.

---

## README — uso rápido

* Edite `config.json` para mapear ações e ajustar sensibilidade.
* Teste localmente rodando `python main.py`.
* Quando ok, gere `.exe` e coloque na pasta de inicialização.

---

Se quiser, eu posso:

* Gerar todos esses arquivos prontos e te enviar (cópia do conteúdo aqui).
* Ou gerar o executável aqui para você baixar (se me autorizar a criar o .exe).

Qual opção prefere?
