# CRUD-completo
CRUD completo em flask, com sistema de login, gerenciamento de usuários registrados, além de todas as funcionalidades exigidas de um CRUD, possui também gráficos e possibilidade de impressão de relatórios das informações que estão no banco de dados.

## Começando

Para executar o projeto, será necessário instalar os seguintes programas:

- [Python: Necessário para executar o projeto](https://www.python.org/downloads/)
- pip para gerenciamento de pacotes e dependências

## Rodando o projeto

Para rodar o projeto, é necessário clonar o projeto do GitHub num diretório de sua preferência:

```shell
cd "diretorio de sua preferencia"
git clone https://github.com/lucasslago1/CRUD-completo.git
```
Agora, crie uma virtual environment no diretório raiz do projeto para instalar as dependências apenas na máquina virtual:

```shell
cd "diretorio raíz"
python3.7 -m venv env
```
Execute a venv:

```shell
source env/bin/activate
```
Instale as dependências necessárias que estão no requirements.txt:

```shell
pip install -r requirements.txt
```
Crie o banco de dados do projeto:

```shell
python3.7 run.py db init
python3.7 run.py db migrate
python3.7 run.py db upgrade
```
Agora rode o projeto e se divirta :)

```shell
python3.7 run.py runserver
```
