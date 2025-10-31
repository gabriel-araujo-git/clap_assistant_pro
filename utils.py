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
