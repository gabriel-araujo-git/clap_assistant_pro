# Arquitetura do Lynx Assistant

[![Build Status](https://img.shields.io/badge/build-stable-brightgreen.svg)](https://github.com/gabriel-araujo-git/Lynx-Assistant/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](../LICENSE)
[![UI](https://img.shields.io/badge/UI-CustomTkinter-2b9348.svg)](#)

---

## Visão Geral

O Lynx Assistant é construído sobre uma arquitetura modular e extensível, projetada para manter o núcleo leve e facilitar a adição de novas funcionalidades.

```
[Interface (CustomTkinter)] → [CommandEngine] → [Sistema / Browser]
```

Cada camada é responsável por uma parte distinta do funcionamento do aplicativo:

1. **Interface (UI)** – captura a entrada do usuário e exibe resultados.  
2. **CommandEngine** – interpreta o texto e mapeia para uma ação.  
3. **Executor** – executa o comando correspondente no sistema operacional.

---

## Estrutura de Pastas

| Caminho | Responsabilidade |
|----------|------------------|
| `assistant_ui.py` | Interface principal, baseada em CustomTkinter |
| `command_engine.py` | Núcleo de interpretação e execução de comandos |
| `core/` | Funções auxiliares e módulos internos |
| `assets/` | Ícones, imagens e arquivos de tema |
| `main.py` | Ponto de entrada do aplicativo |
| `docs/` | Documentação e guias técnicos |

---

## Componentes Principais

### Interface (`assistant_ui.py`)
- Baseada em **CustomTkinter**
- Fornece campo de entrada de comandos e histórico
- Controla a janela e o ícone na bandeja via **PyStray**

### Engine (`command_engine.py`)
- Interpreta instruções em linguagem natural
- Realiza o mapeamento de sinônimos
- Executa comandos via `subprocess` e `webbrowser`

### Core
- Contém funções de suporte, tratadores de erros e utilitários
- Estruturado para expansão futura de módulos “insideof”

---

## Dependências Técnicas

- **Python** 3.10+  
- **CustomTkinter** – interface moderna baseada em Tkinter  
- **PyStray** – gerenciamento do ícone de bandeja  
- **Pillow** – manipulação de ícones e imagens  
- **subprocess / webbrowser** – execução de programas e navegação  

---

## Extensibilidade

O design modular permite:
- Adição de novos comandos sem alterar o núcleo.
- Criação de módulos externos para automações específicas.
- Integração futura com APIs de IA ou serviços de voz.
