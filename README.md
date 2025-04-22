# 📧 ia-limpa-email

**ia-limpa-email** é uma solução automatizada que utiliza Inteligência Artificial para organizar, classificar e manter sua caixa de entrada limpa de forma inteligente e eficiente. Foco total em produtividade e menos ruído digital no seu dia a dia.

## 🚀 Funcionalidades

- Classifica automaticamente e-mails por relevância (trabalho, pessoal, promoções, redes sociais, etc.)
- Remove ou arquiva e-mails considerados irrelevantes, spam ou duplicados
- Cancela inscrições de e-mails promocionais indesejados (em desenvolvimento)
- Detecta e trata e-mails na pasta de spam, evitando que algo importante se perca
- Gera logs e relatórios para acompanhamento das ações realizadas pela IA

## 🧐 Tecnologias Utilizadas

- Python 3.x
- Bibliotecas: `imaplib`, `email`, `nltk`, `scikit-learn`, `openai`
- Integração com API do Gmail (via OAuth2)
- Mecanismo de classificação usando NLP e embeddings de linguagem

## ⚙️ Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/Lucasmrc81/ia-limpa-email.git
   ```

2. Acesse o diretório do projeto:
   ```bash
   cd ia-limpa-email
   ```

3. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 📄 Uso

1. Configure o arquivo `credentials.json` com as credenciais da API do Gmail (OAuth2)
2. Adicione sua chave da OpenAI no arquivo `.env`
3. Execute o sistema:
   ```bash
   python main.py
   ```

O sistema se conectará à sua conta de e-mail, classificará as mensagens, moverá o que for irrelevante, e emitirá relatórios.

## 🔐 Segurança

- Certifique-se de que os arquivos `.env`, `credentials.json` e `token.json` estão no `.gitignore`
- Nunca compartilhe essas informações ou envie para o GitHub

## 🛠️ Contribuições

Pull requests são bem-vindos! Envie sugestões, melhorias ou relatórios de bug via [Issues](https://github.com/Lucasmrc81/ia-limpa-email/issues).

## 📃 Licença

Este projeto é licenciado sob a [MIT License](LICENSE).

---

Acesse o repositório oficial: [https://github.com/Lucasmrc81/ia-limpa-email](https://github.com/Lucasmrc81/ia-limpa-email)

Dominando o caos da sua caixa de entrada com IA. Simples assim. ✅

