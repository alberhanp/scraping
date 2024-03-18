# Scraping sem Selenium

## Propósito

Este projeto é capaz de fazer scraping de dados sem usar um automatizador de navegador.
Ele é focado em um site específico.

## Como Executar usando Docker

### Pré-requisitos
- Docker/Docker-Compose

### Instruções

1. Instale o Docker/Docker-Compose se não tiver ainda.
2. Vá até o diretório raiz do projeto, onde se encontra o arquivo docker-compose.yml .
3. Execute o seguinte comando:
   - `docker compose up -d`
4. Após isso, a API para fazer scraping e consultar dados estará disponível na porta 8080.

## Como Executar localmente

### Pré-requisitos
- Python 3.x
- Virtual Environment (virtualenv)
- Conexão com um banco mongoDB (pode se usar o banco dockerizado disponível acima, consultar as credencias no arquivo docker-compose.yml)

### Instruções

1. **Instalação do Python**:
   - Faça o download e instale o Python [aqui](https://www.python.org/downloads/).

2. **Criação do Ambiente Virtual**:
   - Execute `python -m venv venv` para criar um ambiente virtual.
   - Ative o ambiente virtual: 
     - Windows: `venv\Scripts\activate`
     - Linux/MacOS: `source venv/bin/activate`

3. **Instalação das Dependências**:
   - Execute `pip install -r requirements.txt`
  
4. **Rodando o projeto**
   - Certifique-se que o .env está com as credencias certas para o seu banco.
   - Uma vez no diretório raiz do projeto, execute o seguinte comando:
       - `pyhton3 main.py`

---

Este README oferece um guia básico para iniciar o projeto. Para mais detalhes, consulte o desenvolvedor:

- Albert Hanchuck: +55 35 99953 9008
