
# Proposta: Funcionalidade de Lançamento de Notas

## Why

Atualmente, o sistema não permite que professores lancem notas para atividades dos alunos. Esta funcionalidade é essencial para a gestão acadêmica, permitindo o acompanhamento do desempenho dos estudantes.

## What Changes

Para habilitar o lançamento de notas, as seguintes mudanças são propostas:

1.  **Nova Tabela `academic_tasks`**: Uma nova tabela será criada para armazenar as atividades acadêmicas (ex: provas, trabalhos). Sem ela, não há onde associar as notas.
2.  **Nova Tabela `activity_grades`**: Será criada uma tabela para armazenar as notas, vinculando um aluno (`user_id`), uma atividade (`task_id`), a nota atribuída, e o professor que a lançou.
3.  **Nova API `POST /activity_grades`**: Um novo endpoint será criado para permitir que um professor (usuário com role apropriada) submeta uma nota para um aluno em uma atividade específica.

## Impact

- **Backend**: Novas tabelas e um novo endpoint de API serão adicionados.
- **Frontend**: A interface precisará ser desenvolvida para consumir a nova API, permitindo que professores visualizem atividades e lancem as notas dos alunos.
- **Usuários**: Professores poderão registrar o desempenho dos alunos. Alunos poderão (em uma futura funcionalidade) visualizar suas notas.
