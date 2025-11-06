# Lynx Assistant

O **Lynx Assistant** é um assistente pessoal inteligente projetado para
otimizar fluxos de trabalho no Windows. Com uma interface leve e
moderna, o Lynx permite executar comandos de automação diretamente por
texto, abrindo aplicações e sites corporativos instantaneamente.

------------------------------------------------------------------------

## 🚀 Visão Geral

Desenvolvido em **Python** com **CustomTkinter**, **PyStray** e
integração nativa com o sistema operacional, o Lynx Assistant foi criado
para rodar discretamente em segundo plano, acessível a qualquer momento
a partir da bandeja do sistema.

Ideal para profissionais que trabalham em ambientes corporativos com
múltiplas ferramentas e precisam de acesso rápido a sistemas internos
como o *Infor LN Studio*, portais web e IDEs.

------------------------------------------------------------------------

## 🧠 Recursos Principais

-   Interface moderna e compacta (CustomTkinter)
-   Execução rápida de comandos personalizados
-   Ícone na bandeja do sistema (PyStray)
-   Atalhos e sinônimos para comandos
-   Compatível com Windows 10 e 11

------------------------------------------------------------------------

## 🗣️ Comandos Disponíveis

  ------------------------------------------------------------------------
  Categoria            Comando Principal              Sinônimos
  -------------------- ------------------------------ --------------------
  **VSCode**           abrir vscode                   vscode, code, vs

  **LN Studio**        abrir ln                       ln, studio ln,
                                                      lnstudio, aln,
                                                      lnstd, std

  **LN Teste**         abrir ln teste                 ln teste, alnteste,
                                                      teste ln, lntst

  **LN Produção**      abrir ln prd                   ln prd, alnprd,
                                                      lnprod, ln produção,
                                                      prd ln

  **Navegador**        abrir navegador                abrir chrome,
                                                      navegador, chrome,
                                                      abrir web
  ------------------------------------------------------------------------

------------------------------------------------------------------------

## ⚙️ Instalação

1.  Instale o Python 3.12 ou superior.

2.  Instale as dependências:

    ``` bash
    pip install customtkinter pystray pillow
    ```

3.  Execute o arquivo principal:

    ``` bash
    python assistant_ui.py
    ```

4.  O Lynx Assistant será iniciado e ficará visível na bandeja do
    sistema.

------------------------------------------------------------------------

## 💡 Dicas de Uso

-   O campo de entrada aceita variações dos comandos (sinônimos).
-   A janela pode ser minimizada; o ícone permanecerá ativo na bandeja.
-   Pode ser configurado para iniciar junto com o Windows (opcional).

------------------------------------------------------------------------

## 🧩 Estrutura do Projeto

    LynxAssistant/
    ├── assistant_ui.py      # Interface gráfica principal
    ├── command_engine.py    # Mecanismo de execução de comandos
    ├── assets/              # Ícones e imagens
    ├── README.md            # Documentação
    └── .gitignore           # Ignora arquivos temporários

------------------------------------------------------------------------

## 🧰 Tecnologias

-   Python 3.12+\
-   CustomTkinter\
-   PyStray\
-   Pillow

------------------------------------------------------------------------

## 📘 Licença

Distribuído sob a licença **MIT**.\
© 2025 Microsoft Style Project --- inspirado em experiências de
produtividade corporativa.

------------------------------------------------------------------------

## 👨‍💻 Autor

**Gabriel Araújo**\
Desenvolvedor de soluções em Inteligência Artificial e automação de
fluxos de trabalho.
