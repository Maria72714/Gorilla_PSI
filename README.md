# 🦍 Projeto Gorilla

Repositório destinado ao **Projeto Gorilla**, desenvolvido para a disciplina de **PSI (Programação de Sistemas de Informação)**.

---

## 📁 Estrutura do Repositório

> Organização atual dos arquivos e diretórios do projeto:

- `app/` – Arquivos Python principais (rotas, lógica da aplicação Flask)
- `templates/` – Arquivos HTML com templates Jinja2
- `static/` – Arquivos estáticos (CSS e imagens)
- `requirements.txt` – Lista de dependências do projeto Python
- `README.md` – Documentação do projeto (este arquivo)

---

## 👥 Equipe e Contribuições

### 🧑‍💻 Eduardo
- Estruturação do projeto Flask
- 

### 🧑‍💻 José Abílio
- 
- 

### 🧑‍💻 Lucas
- 
- 

### 🧑‍💻 Maria Luiza
- 
- 


---

## 💡 Objetivo do Projeto

Desenvolver uma aplicação web para a loja fictícia de suplementos **Gorilla**, utilizando o framework **Flask**. O sistema permite:

- Cadastro e login de usuários com autenticação segura;
- Navegação e visualização de produtos;
- Gerenciamento de carrinho e pedidos.

A aplicação utiliza **SQLite** como banco de dados local, aplicando conceitos de rotas, sessões, templates com Jinja2 e autenticação com Flask-Login.

---

## ✅ Requisitos do Projeto

### 🔧 Requisitos Funcionais (RF)

- **RF01** – O usuário deve poder se cadastrar no sistema.
- **RF02** – O usuário deve poder realizar login e logout.
- **RF03** – O usuário deve poder visualizar a lista de suplementos disponíveis.
- **RF04** – O usuário deve poder adicionar e remover produtos do carrinho.
- **RF05** – O usuário deve poder finalizar a compra.

### 📈 Requisitos Não Funcionais (RNF)

- **RNF01** – O sistema deve ser desenvolvido com o framework **Flask** em **Python**.
- **RNF02** – O banco de dados utilizado deve ser **SQLite**.
- **RNF03** – A interface deve ser acessível por navegadores modernos (Google Chrome, Firefox etc.).
- **RNF04** – O sistema deve utilizar criptografia (hash) para armazenar senhas.
- **RNF05** – O sistema deve ser responsivo e funcionar bem em dispositivos móveis e desktops.
- **RNF06** – O código-fonte deve estar versionado e disponível no GitHub.

---

## 🛠️ Tecnologias Utilizadas

- Python / Flask
- HTML, CSS
- SQLite
- Jinja2 (templates)
- Flask-Login
- Werkzeug (hash de senhas)

---

## 📌 Instruções para Executar

```bash
# Clone o repositório
git clone https://github.com/Maria72714/Gorilla_PSI

# Acesse a pasta do projeto
cd Gorilla_PSI

# Crie e ative um ambiente virtual (opcional, mas recomendado)
python -m venv env
source env/bin/activate        # Linux/macOS
env\Scripts\activate           # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o projeto
python app.py

