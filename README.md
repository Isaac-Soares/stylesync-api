# 🛍️ StyleSync API

Uma API RESTful desenvolvida com **Flask** e **MongoDB**, projetada com foco em organização, modularidade, segurança e escalabilidade.

Este projeto demonstra a implementação de uma arquitetura utilizando o padrão **Application Factory**, integração com banco de dados NoSQL, autenticação baseada em **JWT** e testes automatizados.

## 🚀 Tecnologias Utilizadas

* **Python 3**
* **Flask** — Framework web para desenvolvimento do backend
* **MongoDB & PyMongo** — Banco de dados NoSQL
* **PyJWT** — Geração e validação de tokens JWT
* **Pytest** — Implementação de testes automatizados
* **Python-dotenv** — Gerenciamento de variáveis de ambiente

## ⚙️ Destaques da Arquitetura

### 🏗️ Application Factory

A aplicação utiliza o padrão **Application Factory** através da função `create_app()`.

Essa abordagem permite:

* Maior modularidade do projeto
* Facilidade na criação de diferentes ambientes
* Melhor organização da aplicação
* Facilidade na execução de testes
* Maior escalabilidade do código

### 🔐 Autenticação e Segurança

Implementação de autenticação baseada em **JSON Web Tokens (JWT)**.

O projeto utiliza decoradores customizados, como:

```python
@token_required
```

para proteger rotas privadas.

O sistema também possui tratamento para situações como:

* Tokens expirados
* Tokens inválidos
* Tokens malformados
* Ausência de autenticação

### 📄 Processamento de CSV

O projeto permite a importação e processamento de arquivos **CSV diretamente em memória**, reduzindo operações desnecessárias de leitura e escrita no disco.

Essa abordagem ajuda a otimizar o processamento dos dados durante a execução da API.

### 🧪 Testes Automatizados

O projeto utiliza **Pytest** para a criação de testes automatizados.

Os testes abrangem funções utilitárias e regras de negócio da aplicação, contribuindo para maior confiabilidade e facilidade de manutenção do código.

### 🔧 Variáveis de Ambiente

As configurações sensíveis da aplicação são carregadas através de variáveis de ambiente utilizando **Python-dotenv**.

Dessa forma, informações como credenciais do banco de dados e chaves secretas não precisam ser armazenadas diretamente no código-fonte.

## 🛠️ Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e executar a API na sua máquina.

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
cd NOME_DO_REPOSITORIO
```

### 2. Crie e ative um ambiente virtual

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo chamado `.env` na raiz do projeto.

Adicione as configurações necessárias:

```env
MONGO_URI=mongodb://localhost:27017/stylesync
SECRET_KEY=sua_chave_secreta_aqui
```

> ⚠️ **Importante:** nunca envie o arquivo `.env` para o GitHub. Adicione `.env` ao seu `.gitignore` para evitar o vazamento de credenciais e chaves secretas.

### 5. Execute a aplicação

```bash
python run.py
```

A aplicação estará disponível no endereço configurado pelo servidor Flask.

## 🧪 Executando os Testes

Para executar a suíte de testes automatizados, utilize:

```bash
pytest
```

Caso queira obter informações mais detalhadas sobre a execução dos testes:

```bash
pytest -v
```

## 📁 Estrutura do Projeto

Uma possível estrutura do projeto é:

```text
.
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── utils/
├── tests/
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> A estrutura acima é apenas um exemplo. Ajuste os nomes dos diretórios e arquivos de acordo com a estrutura real do projeto.

## 🔒 Segurança

Este projeto utiliza variáveis de ambiente para armazenar informações sensíveis.

Antes de publicar o código, certifique-se de que arquivos contendo credenciais, como `.env`, não estejam sendo enviados para o repositório.

Exemplo de `.gitignore`:

```gitignore
venv/
.env
__pycache__/
*.pyc
.pytest_cache/
```

## 👨‍💻 Autor

**Isaac Faria Soares**

Estudante de Ciência da Computação no **UniCEUB**.

[LinkedIn](https://www.linkedin.com/in/isaac-faria-soares/)

---

⭐ Se este projeto foi útil para você, considere deixar uma estrela no repositório.
