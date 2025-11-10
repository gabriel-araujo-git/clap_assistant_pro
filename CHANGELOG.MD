<!-- Banner central -->
<div align="center">
  <img src="https://img.shields.io/badge/Lynx%20Assistant-%23000000.svg?style=for-the-badge&logo=python&logoColor=white" height="30"/>
  <img src="https://img.shields.io/badge/CHANGELOG-%23181717.svg?style=for-the-badge&logo=github&logoColor=white" height="30"/>
</div>

<h1 align="center">Histórico de Versões — Lynx Assistant</h1>

<p align="center">
  <b>Assistente desktop inteligente e open source</b>.<br/>
  Automação local, privada e extensível, feita para produtividade real.
</p>

---

## 📜 Sobre este documento

Este changelog segue o padrão <a href="https://keepachangelog.com/pt-BR/1.0.0/">Keep a Changelog</a>  
e adota o <a href="https://semver.org/lang/pt-BR/">Versionamento Semântico</a> (SemVer).

Cada versão aqui representa um marco funcional e de design do Lynx — desde a fundação do projeto até sua primeira versão pública estável.

---

## 🦊 v1.1.0 — 07 de Novembro de 2025
### Atualização de Interface e Novos Recursos

#### Adicionado
- Nova interface aprimorada, mais leve e responsiva.  
- Adição de comandos internos e externos pré-configurados.  
- Suporte a **busca em sites** e funções de pesquisa personalizadas.  
- Inclusão de **sinônimos de comandos** (ex: “abrir navegador” = “abrir chrome”).  
- Novos comandos nativos: **Outlook**, **VSCode**, **LinkedIn**, entre outros.  
- Sistema de gerenciamento visual de comandos.  

#### Corrigido
- Estabilizada a função `show_add_command`.  
- Correção da seleção do tipo de comando (interno/externo).  
- Ajustes no salvamento e atualização do arquivo `commands.json`.

#### Documentação
- Revisão completa do `README.md` com estrutura profissional e layout responsivo.  
- Criação dos arquivos:
  - `CONTRIBUTING.md`
  - `CHANGELOG.md`
  - `LICENSE`
- Ajuste do texto de filosofia e do padrão visual geral do projeto.

---

## 🚀 v1.0.0 — 30 de Outubro de 2025
### Lançamento Público Inicial

#### Adicionado
- Engine de comandos modular (`CommandEngine`).  
- Interface inicial em **CustomTkinter** com tema escuro.  
- Execução de **programas locais** e **sites externos**.  
- Persistência local de comandos via `commands.json`.  
- Integração com bandeja do sistema via **PyStray**.  
- Tela de ajuda e painel de adição de comandos.  
- Estrutura documental inicial (`README`, `LICENSE`, `requirements.txt`).

#### Melhorado
- Separação entre **Engine** e **UI** para facilitar expansão modular.  
- Otimização do carregamento e execução de comandos.

---

## 🔮 Planejado — Próximas Versões (v1.2 e além)

| Categoria | Descrição |
|:-----------|:-----------|
| ⚙️ **Funcionalidades** | Dashboard para edição visual de comandos |
| 🗣️ **Interação** | Suporte a comandos de voz e IA local |
| 💾 **Infraestrutura** | Atualizações automáticas e instalador oficial |
| 🌐 **Integrações** | Suporte a APIs externas e sincronização opcional |
| 🧩 **Customização** | Exportação/importação de comandos personalizados |

---

## 🧭 Linha do Tempo

| Data | Marco | Descrição |
|:------|:-------|:-----------|
| **30/10/2025** | v1.0.0 | Primeira versão funcional e pública |
| **06/11/2025** | v1.1.0 (pre-release) | Interface redesenhada e novos comandos |
| **07/11/2025** | v1.1.0 (final) | Versão estável e documentada |
| **10/11/2025** | release preparado | Inclusão de documentação completa e empacotamento |

---

<p align="center">
  <img src="https://img.shields.io/badge/Build%20Fast-Think%20Slow-000000?style=for-the-badge" height="28"/>
</p>

<p align="center">
  <i>“Código é só o início — a utilidade é o que o transforma em produto.”</i>
</p>
