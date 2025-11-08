# 🦊 Lynx

> O poder dos comandos rápidos, na ponta dos seus dedos.

O **Lynx** é um assistente desktop inteligente que executa comandos e abre programas, sites e ambientes com naturalidade.  
Diga “ln teste”, “abrir VSCode” ou “abrir YouTube” — e ele faz o resto.

---

## ✨ Destaques

- ⚡ **Comandos rápidos e naturais** — sem sintaxe complicada.  
- 🧠 **Aprendizado adaptável** — você adiciona seus próprios atalhos.  
- 🎨 **Interface moderna (CustomTkinter)** — leve, escura e elegante.  
- 🔗 **Integração com programas e sites** — do VSCode ao LinkedIn.  
- 💾 **Persistência local** — seus comandos ficam salvos em `commands.json`.  

---

## 🖼️ Interface

| Tela Principal | Ajuda Expandida | Adicionar Comando |
|----------------|------------------|-------------------|
| ![Main](docs/screenshot_main.png) | ![Help](docs/screenshot_help.png) | ![Add](docs/screenshot_add.png) |

---

## 💻 Como usar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seuusuario/lynx.git
   cd lynx
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o Lynx:**
   ```bash
   python assistant_ui.py
   ```

O aplicativo iniciará em modo janela e adicionará um ícone na bandeja do sistema.  
Você pode escondê-lo e reabrir a qualquer momento.

---

## 🧩 Estrutura de diretórios

```
lynx/
│
├── assistant_ui.py        # Interface principal (UI + Command Engine)
├── commands.json          # Banco local de comandos
├── requirements.txt
├── LICENSE
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
└── docs/
    ├── screenshot_main.png
    ├── screenshot_help.png
    └── screenshot_add.png
```

---

## 🧠 Como adicionar novos comandos

No app, clique em **“Adicionar”** e defina:
- tipo: interno (programa) ou externo (site)  
- nome e palavras-chave  
- caminho (exe) ou URL

O Lynx salva tudo automaticamente no arquivo `commands.json`.

---

## 🛠️ Tecnologias

- **Python 3.10+**
- **CustomTkinter**
- **PyStray**
- **Pillow**
- **Subprocess / Webbrowser**

---

## 📜 Licença

Distribuído sob a [MIT License](LICENSE).

---

## 🤝 Contribuindo

Quer ajudar a expandir o Lynx?  
Veja nosso [guia de contribuição](CONTRIBUTING.md) e envie seu PR!

---

## 💬 Sobre o projeto

O Lynx nasceu da vontade de automatizar ações simples do dia a dia de um desenvolvedor — abrir o VSCode, acessar o ambiente de teste, entrar em sites e ferramentas com um só comando.

Criado por [Gabriel Araújo](https://github.com/seuusuario), e aberto à comunidade para crescer junto.

---

> _“Grandes ferramentas nascem de pequenas dores diárias.”_
