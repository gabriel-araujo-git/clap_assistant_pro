<!-- Banner central -->
<div align="center">
  <img src="https://img.shields.io/badge/Lynx%20Assistant-Changelog-%231a1a1a.svg?style=for-the-badge&logo=github&logoColor=white" height="32"/>
  <img src="https://img.shields.io/badge/Versioning-SemVer%20Compliant-%23282828.svg?style=for-the-badge&logo=semanticrelease&logoColor=white" height="32"/>
  <img src="https://img.shields.io/badge/Open%20Source-%23181717.svg?style=for-the-badge&logo=opensourceinitiative&logoColor=white" height="32"/>
</div>

<h1 align="center">Histórico de Versões — Lynx Assistant</h1>

---

## Sobre este documento

Este changelog segue o padrão <a href="https://keepachangelog.com/pt-BR/1.0.0/">Keep a Changelog</a>  
e adota o <a href="https://semver.org/lang/pt-BR/">Versionamento Semântico</a> (SemVer).

Cada versão registrada representa um marco funcional, técnico e visual do Lynx Assistant.

---

## [1.2.1] – 2025-11-20

### Added
- Implementado o novo **Command Engine baseado em JSON**, permitindo definição estruturada e expansível de comandos.
- Criado o **Command Orchestrator** para gerenciar a execução dos comandos JSON, melhorando a arquitetura interna.
  *(commit: #33 – feat(core): implement JSON-based command engine and orchestrator)*

### Changed
- Refatoração ampla dos imports do projeto, removendo duplicações e comentários desnecessários para melhorar organização e manutenção.
  *(commit: #34 – Refactor imports and remove unnecessary comments)*

### Fixed
- Corrigido o caminho do arquivo JSON utilizado pela função `load_json`, garantindo carregamento correto dos comandos.
  *(commit: #35 – Update JSON file path in load_json function)*


## [1.2.0] – 2025-11-14

### Added  
- Refatorada a interface **“Adicionar Comando”** para usar CustomTkinter, com layout mais intuitivo, tema escuro e responsivo.  
- Implementada nova funcionalidade de **gerenciamento de palavras-chave** (keywords) ao adicionar comandos: permite definir múltiplos termos de ativação.  
- Adicionado salvamento em tempo real para `commands.json` na tela de adição de comando, sem necessidade de reiniciar o aplicativo.  
- Refatorada a interface **“Ajuda”** com visual aprimorado, links diretos para documentação e melhoria na navegação das seções de suporte.  
- Atualizada a lógica de filtragem/seleção de comandos recentes dentro da UI para facilitar reutilização.

### Changed  
- Reorganizada a estrutura da tela “Adicionar Comando”: agora há separação clara entre comandos internos (programas) e externos (sites), com radiobuttons estilizados.  
- Ajustes de UX: janelas “Toplevel” agora possuem `-topmost` habilitado, garantindo que fiquem em foco durante inclusão de comandos.  
- Código reorganizado para otimizar importações duplicadas (ex: múltiplas importações de `filedialog`, `messagebox`).  
- Atualizado tratamento de erros/validações na UI de adição: verificação de formato de URL, existência de caminho de arquivo, e alertas mais claros aos usuários.

### Fixed  
- Corrigido bug onde ao sair da janela “Adicionar Comando”, o foco voltava para o aplicativo principal e causava scroll indesejado.  
- Ajustado problema onde alguns campos da UI apareciam com proporção incorreta ou sobreposição em monitores múltiplos.  
- Melhorada a estabilidade do carregamento de `commands.json` após adição de comando, evitando duplicações ou sobrescritas indevidas.

### Documentation  
- Atualizada a seção “Uso” no `docs/usage.md` para refletir as novas telas.  
- Incluída captura de tela da interface “Adicionar Comando” atualizada no diretório `docs/`.  
- `README.md` atualizado para mencionar suporte de keywords e melhor experiência UX nas telas de ajuda/comando.



## [1.1.0] - 2025-11-13

### Added
- Adicionado `codeql.yml` para integração de análise de segurança automatizada.
- Adicionado `dependabot.yml` para controle e atualização de dependências.
- Revisado o `SECURITY.md` com novas diretrizes e seções.
- Incluídos novos arquivos de documentação técnica:
  - `docs/setup.md`
  - `docs/usage.md`
  - `docs/architecture.md`
  - `docs/roadmap.md`
- Preparado o **Manual de Comandos (Wiki / HTML)** para futura publicação via GitHub Pages.

### Changed
- **Refatorada a estrutura do projeto** — reorganização de pastas, nomes e arquitetura interna  
  *(commits: Refactor/estrutura projeto #13, #16)*
- Atualizado o pipeline do **Dependabot** com novas regras.
- Ajustes gerais nas configurações internas e documentação complementar.

### Fixed
- Corrigidos caminhos e nomes de pastas incorretos *(#10)*.
- Pequenas correções de estrutura e formatação em arquivos de suporte e documentação.

## v1.1.1 — 12 de Novembro de 2025
### Melhorias
- Adicionado salvamento dinâmico de comandos personalizados, permitindo uso imediato sem reiniciar o aplicativo.

### Correções
- Corrigido o problema em que o processo do Lynx continuava executando em segundo plano após o fechamento.
- Implementado encerramento completo do tray e das threads ao sair do aplicativo, garantindo liberação total de recursos.


## v1.1.0 — 07 de Novembro de 2025
### Atualização de Interface e Novos Recursos

#### Adicionado
- Interface aprimorada, mais leve e responsiva.  
- Comandos internos e externos pré-configurados.  
- Suporte a busca em sites e funções de pesquisa personalizadas.  
- Inclusão de sinônimos de comandos (ex: “abrir navegador” = “abrir chrome”).  
- Novos comandos nativos: Outlook, VSCode, LinkedIn, entre outros.  
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
- Ajuste do texto de filosofia e padronização visual geral.

---

## v1.0.0 — 30 de Outubro de 2025
### Lançamento Público Inicial

#### Adicionado
- Engine de comandos modular (`CommandEngine`).  
- Interface inicial em CustomTkinter com tema escuro.  
- Execução de programas locais e sites externos.  
- Persistência local de comandos via `commands.json`.  
- Integração com bandeja do sistema via PyStray.  
- Tela de ajuda e painel de adição de comandos.  
- Estrutura documental inicial (`README`, `LICENSE`, `requirements.txt`).

#### Melhorado
- Separação entre Engine e UI para facilitar expansão modular.  
- Otimização do carregamento e execução de comandos.

---

## Planejado — Próximas Versões (v1.2 e além)

| Categoria | Descrição |
|:-----------|:-----------|
| Funcionalidades | Dashboard para edição visual de comandos |
| Interação | Suporte a comandos de voz e IA local |
| Infraestrutura | Atualizações automáticas e instalador oficial |
| Integrações | Suporte a APIs externas e sincronização opcional |
| Customização | Exportação/importação de comandos personalizados |

---

## Linha do Tempo

| Data | Marco | Descrição |
|:------|:-------|:-----------|
| 30/10/2025 | v1.0.0 | Primeira versão funcional e pública |
| 06/11/2025 | v1.1.0 (pre-release) | Interface redesenhada e novos comandos |
| 07/11/2025 | v1.1.0 (final) | Versão estável e documentada |
| 10/11/2025 | Release final | Inclusão de documentação e empacotamento |

---

<p align="center">
  <img src="https://img.shields.io/badge/Build%20Fast-Think%20Slow-000000?style=for-the-badge" height="28"/>
</p>

<p align="center">
  <i>"Código é apenas o início — a utilidade é o que o transforma em produto."</i>
</p>
