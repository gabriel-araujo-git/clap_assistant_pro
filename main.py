from command_engine import CommandEngine
from commands import system_commands, web_commands

engine = CommandEngine()
engine.register("abrir", system_commands.COMMANDS)
engine.register("pesquisar", web_commands.COMMANDS)

print("Assistente pronto! Digite seu comando (ou 'sair'):")

while True:
    cmd = input("> ")
    if cmd.lower() in ["sair", "exit"]:
        break
    result = engine.interpret(cmd)
    print(result)
