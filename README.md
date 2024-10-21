# workshop_api

Este projeto faz parte de um workshop ministrado na Unicesumar sobre Backend, utilizando API REST com FastAPI e MongoDB.

## Gerenciamento de Tarefas em Equipe (Task Manager API)

### Descrição Geral
A aplicação tem como objetivo permitir o gerenciamento de projetos e tarefas dentro de equipes. Cada usuário pode criar projetos e adicionar tarefas a eles. As tarefas podem ser atribuídas a membros da equipe, com prazos e status definidos. Os membros da equipe podem ser gerenciados em cada projeto, permitindo uma distribuição eficiente das responsabilidades.

### Entidades Principais

- **Usuário**: Pessoas que utilizam o sistema. Eles podem criar projetos e tarefas e gerenciar membros.
- **Projeto**: Um conjunto de tarefas organizadas para atingir um objetivo específico. Cada projeto tem uma lista de tarefas e uma equipe associada.
- **Tarefa**: As atividades específicas que precisam ser realizadas dentro de um projeto. Cada tarefa tem um status, um prazo e pode ser atribuída a um membro da equipe.
- **Equipe/Membro**: Conjunto de usuários que trabalham em um projeto. As tarefas podem ser atribuídas a diferentes membros da equipe.

### Regras de Negócio

#### Autenticação e Autorização

- Apenas usuários autenticados podem criar projetos, tarefas e gerenciar membros da equipe.
- O acesso a projetos e tarefas é restrito ao usuário que criou o projeto e aos membros da equipe.
- A autenticação será feita via JWT (JSON Web Token) para garantir que apenas usuários autorizados realizem certas ações.

#### Gerenciamento de Projetos

- Cada usuário pode criar e gerenciar múltiplos projetos.
- Um projeto deve ter, no mínimo, um nome e pode conter uma descrição opcional.
- Um projeto pode conter várias tarefas e deve permitir a adição de membros da equipe que trabalharão nele.
- Um projeto pode ser atualizado ou excluído, desde que o usuário seja o criador ou tenha permissão.

#### Gerenciamento de Tarefas

- As tarefas estão associadas a um projeto específico e devem ter um título, uma descrição (opcional), um prazo e um status.
- O status de uma tarefa pode ser: `A Fazer`, `Em Andamento`, ou `Concluída`.
- Uma tarefa pode ser atribuída a um membro da equipe ou pode ficar sem atribuição (a ser decidida depois).
- As tarefas podem ser atualizadas (por exemplo, mudar o status, alterar o prazo ou reatribuir a outro membro).
- O criador da tarefa e os membros atribuídos podem excluí-la, desde que tenham permissão.

#### Gerenciamento de Membros

- O criador de um projeto pode adicionar e remover membros da equipe.
- Apenas membros de um projeto podem ser atribuídos a tarefas daquele projeto.
- Membros podem ser visualizados e gerenciados pelo criador ou administradores do projeto.

#### Regras de Atribuição de Tarefas

- Cada tarefa pode ser atribuída a apenas um membro da equipe por vez.
- Um membro pode ter várias tarefas atribuídas a ele, mas não pode estar atribuído à mesma tarefa mais de uma vez.
- As tarefas podem ser reatribuídas a outros membros, desde que o criador ou administrador da equipe faça essa alteração.

#### Validação de Prazo de Tarefas

- O prazo de uma tarefa não pode ser anterior à data de criação.
- O sistema deve permitir listar as tarefas em ordem de prioridade ou por prazo próximo, facilitando a organização.

## Sobre o Projeto Python

- O que é o `requirements.txt`?
    - São arquivos que contém uma lista de dependências de um projeto.
    - Cada linha do arquivo contém o nome de uma dependência e sua versão.
    - Exemplo:
        ```
        Flask==1.1.2
        requests==2.25.1
        ```

- Para que serve?

    - Servem para que possamos instalar todas as dependências de um projeto de uma só vez.
    - Exemplo:
        ```
        pip install -r requirements.txt
        ```

## O que é o Dockerfile?

- Para que serve?

    - Serve para criar uma imagem Docker.
    - Uma imagem Docker é um arquivo que contém todas as dependências de um projeto.
    - Exemplo:
        ```
        FROM python:3.8
        WORKDIR /app
        COPY . /app
        RUN pip install -r requirements.txt
        CMD ["python", "app.py"]
        ```

- Como criar uma imagem Docker?

    - Para criar uma imagem Docker, basta executar o seguinte comando:
        ```
        docker build -t workshop_api .
        ```

- Como rodar os containers Docker deste projeto?

    - Para rodar os containers Docker deste projeto, basta executar os seguintes comandos:
        ```
        cd workshop_api/pythonProject/
        docker-compose up -d
        ```

    - Este comando irá criar e rodar os containers Docker do MongoDB e da API REST em Python.