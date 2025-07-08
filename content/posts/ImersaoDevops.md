---
title: "Imersão DevOps - Google Cloud"
date: 2019-02-27T20:54:51-06:00
draft: false
---

## Este projeto é uma API desenvolvida com FastAPI para gerenciar alunos, cursos e matrículas em uma instituição de ensino.
```
Este projeto é uma API desenvolvida com FastAPI para gerenciar alunos, cursos e matrículas em uma instituição de ensino.
```

## Pré-requisitos
```

    Python 3.10 ou superior instalado
    Git
    Docker

```

## Passos para subir o projeto
```
Crie um ambiente virtual: $ python3 -m venv ./venv
Ative: $ source venv/bin/activate

```

## Instale as dependências:
```
$ pip install -r requirements.txt
```

## Execute a aplicação:
```
uvicorn app:app --reload
```

## Acesse a documentação interativa:
Abra o navegador e acesse:
http://127.0.0.1:8000/docs

Aqui você pode testar todos os endpoints da API de forma interativa.

## Estrutura do Projeto

    app.py: Arquivo principal da aplicação FastAPI.
    models.py: Modelos do banco de dados (SQLAlchemy).
    schemas.py: Schemas de validação (Pydantic).
    database.py: Configuração do banco de dados SQLite.
    routers/: Diretório com os arquivos de rotas (alunos, cursos, matrículas).
    requirements.txt: Lista de dependências do projeto.


    O banco de dados SQLite será criado automaticamente como escola.db na primeira execução.
    Para reiniciar o banco, basta apagar o arquivo escola.db (isso apagará todos os dados).


## Gerando dockerFile

Gerei o arquivo com a ajuda do Gemini Code

```yml
# Usa uma imagem oficial do Python como imagem base
# A versão python:3.10-slim é uma ótima escolha por ter um tamanho reduzido
FROM python:3.10-slim

# Define variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir --upgrade pip -r requirements.txt

# Copia o restante do código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta 8000 para permitir a comunicação com a aplicação
EXPOSE 8000

# Define o comando para executar a aplicação
# Usa 0.0.0.0 para torná-la acessível de fora do contêiner
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

```

## Fazendo Buid da imagem

![HTB](/DockerBuild.png)


## Push para o Docker Hub

![HTB](/dockerpush.png)

## Aplicação no ar com localhost 

![HTB](/localhostDocker.png)