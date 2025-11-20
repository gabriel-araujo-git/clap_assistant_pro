# src/core/orchestrator.py
from core.command_engine import CommandEngine

from core.command_engine import CommandEngine

class Orchestrator:
    def __init__(self):
        self.engine = CommandEngine()

    def handle_input(self, text):
        return self.engine.execute(text)
