<!-- Banner -->
<div align="center">
  <img src="https://img.shields.io/badge/Lynx%20Assistant-Contributing-%231a1a1a.svg?style=for-the-badge&logo=github&logoColor=white" height="32"/>
</div>

<h1 align="center">Guia de Contribuição — Lynx Assistant</h1>

<p align="center">
  O <b>Lynx Assistant</b> é um projeto open source que busca tornar automações de desktop mais acessíveis e eficientes.<br/>
  Toda contribuição é bem-vinda — de pequenas correções a grandes ideias.
</p>

---

## Como contribuir

1. **Fork** o repositório no GitHub.
2. Crie uma nova branch para sua contribuição:
   ```bash
   git checkout -b feature/nome-da-funcionalidade
   ```
3. Faça suas alterações e **teste localmente**:
   ```bash
   python assistant_ui.py
   ```
4. Confirme que o código está limpo e organizado.
5. Envie um **pull request (PR)** com uma descrição clara do que foi alterado.

---

## Diretrizes de código

- Mantenha a consistência de estilo com o restante do código (`PEP8` + nomes descritivos).
- Evite dependências desnecessárias.
- Prefira mensagens de commit claras:
  ```
  feat: adiciona suporte a novos atalhos
  fix: corrige erro ao salvar comandos personalizados
  docs: atualiza README com novas instruções
  ```

---

## Testando suas alterações

Antes de enviar, verifique:
- Se o comando foi adicionado corretamente no `commands.json`.
- Se a interface responde bem a novas opções ou botões.
- Se o engine carrega os novos comandos sem erro.

---

## Dúvidas ou sugestões

Abra uma **issue** descrevendo sua ideia ou problema.  
Todos os feedbacks são bem-vindos — o objetivo é fazer o Lynx crescer com a comunidade!

---

> “Grandes ferramentas nascem de pequenas dores diárias.”
