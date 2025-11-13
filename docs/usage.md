# Uso do Lynx Assistant

[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](#)
[![Interface](https://img.shields.io/badge/UI-CustomTkinter-blue.svg)](#)
[![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey.svg)](#)

---

## Executando Comandos

Digite comandos diretamente na interface principal.  
Alguns exemplos:

```bash
ln teste
abrir vscode
abrir youtube
abrir pasta de projetos
```

---

## Adicionando Novos Comandos

1. Abra o arquivo `command_engine.py`
2. Localize o dicionário de comandos ou sinônimos
3. Adicione um novo mapeamento no formato:

```python
("abrir bloco de notas", "notepad.exe"),
("abrir excel", "excel.exe"),
```
4. Salve e reinicie o Lynx.

---

## Interface

- **Campo de Comando**: onde o usuário digita instruções  
- **Histórico**: exibe comandos recentes  
- **Bandeja do Sistema**: permite ocultar/exibir a janela e sair do aplicativo  

A interface é implementada em **CustomTkinter** e segue um estilo minimalista.

---

## Personalização

- **Temas e cores**: ajustáveis em `assistant_ui.py`  
- **Ícones e imagens**: armazenados em `assets/`  
- **Comportamento da interface**: controlado via variáveis globais em `assistant_ui.py`
