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
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    LOG.info("Encerrado pelo usuário.")
except Exception as e:
    LOG.exception("Erro crítico: %s", e)
    raise
