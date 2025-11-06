# 🦊 Lynx — Desktop Assistant Open Source

O **Lynx** é um assistente desktop leve, rápido e personalizável, criado para simplificar tarefas do dia a dia de desenvolvedores e analistas.  
Com uma interface minimalista construída em **CustomTkinter**, o Lynx interpreta **comandos de texto naturais** e executa ações locais ou na web — como abrir o VSCode, o LN Studio ou ambientes de teste e produção.

> 🚀 Um projeto open source que combina **automação pessoal**, **UX minimalista** e **customização simples via Python**.

---

## 🌟 Principais Recursos

- 🔹 **Interface leve e intuitiva** — uma janela compacta com modo escuro e feedback instantâneo.
- 🔹 **Comandos naturais** — digite “abrir vscode”, “ln teste”, “chrome” ou sinônimos equivalentes.
- 🔹 **Personalização total** — adicione novos comandos ou sinônimos editando uma única classe (`CommandEngine`).
- 🔹 **Integração com bandeja do sistema** — o Lynx fica sempre acessível, sem ocupar espaço na tela.
- 🔹 **Execução segura e local** — nenhum dado é enviado para servidores externos.
- 🔹 **Código 100% open source** — modifique, contribua e compartilhe.

---

## 💡 Exemplo de Uso

Após iniciar o Lynx:

1. Digite no campo de entrada:
   ```
   ln teste
   ```
2. O Lynx abrirá automaticamente o ambiente de testes configurado.
3. Tente também:
   ```
   vscode
   ln prd
   navegador
   bloco de notas
   ```

> Cada comando possui **sinônimos configuráveis**, permitindo variações como “abrir ln teste” ou “abrir vs”.

---

## ⚙️ Instalação e Execução

### 🐍 Pré-requisitos
- Python **3.9+**
- Pip instalado

### 📦 Dependências
Instale as dependências com:
```bash
pip install customtkinter pystray pillow
```

### ▶️ Executando o Lynx
No terminal:
```bash
python assistant_ui.py
```

O Lynx iniciará em modo janela e ficará disponível na **bandeja do sistema** (System Tray).  
Você pode ocultar ou reabrir a interface a qualquer momento.

---

## 🧠 Estrutura do Projeto

```
lynx/
├── assistant_ui.py     # Código principal (UI + Engine)
├── README.md           # Este arquivo
└── requirements.txt    # Dependências (opcional)
```

### Componentes:
- **CommandEngine** → Gerencia comandos, sinônimos e ações.
- **LynxApp** → Interface principal construída com `customtkinter`.
- **Tray Icon** → Ícone residente que permite abrir/fechar o app rapidamente.

---

## 🧩 Adicionando Novos Comandos

Quer expandir o Lynx?  
Edite a classe `CommandEngine` no arquivo `assistant_ui.py`:

```python
("abrir spotify", "spotify", "abrir música"): self.open_spotify
```

E defina a função correspondente:
```python
def open_spotify(self):
    subprocess.Popen("spotify", shell=True)
    return "🎵 Abrindo Spotify..."
```

Pronto! O Lynx agora entende esse novo comando.

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas!  
Para colaborar:

1. Faça um **fork** do repositório  
2. Crie uma branch com sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```
3. Faça o commit das alterações:
   ```bash
   git commit -m "Adiciona comando Spotify"
   ```
4. Envie um **Pull Request**

> Antes de enviar, mantenha o código limpo e siga o estilo existente (PEP8 + emoji feedbacks nos retornos).

---

## 🧭 Roadmap (Ideias Futuras)

- 🔸 Reconhecimento de voz (speech-to-text)
- 🔸 Histórico persistente de comandos
- 🔸 Temas customizáveis
- 🔸 Plugins externos em Python
- 🔸 Integração com APIs locais (ex: Git, Docker, Jira)

---

## 📜 Licença

Distribuído sob a licença **MIT**.  
Você é livre para usar, modificar e distribuir — apenas mantenha os créditos ao projeto.
