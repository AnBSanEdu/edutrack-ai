
# Design Técnico: Tabela `academic_tasks`

## 1. Estrutura de Dados

### Tabela: `academic_tasks`

Esta tabela irá armazenar as tarefas e obrigações acadêmicas que cada aluno registrar no sistema.

- **Arquivo:** `tables/academic_tasks.xs`
- **Justificativa do Schema:**
    - `user_id`: Essencial para garantir que cada tarefa seja associada ao aluno que a criou, permitindo que cada usuário gerencie suas próprias obrigações.
    - `description`, `due_date`: Definidos como opcionais (`?`) para flexibilidade, pois uma tarefa pode ser criada inicialmente apenas com um título.
    - `status`: Inclui um valor padrão (`"pending"`) para simplificar a criação de novas tarefas.

- **Schema:**
  ```xanoscript
  table academic_tasks {
    // Relação com o usuário que criou a tarefa
    int user_id;

    // Relação com a disciplina da tarefa
    int subject_id;

    // Detalhes da tarefa
    text title;
    text description?;
    date due_date?;
    text status?="pending"; // Ex: pending, in-progress, completed
  }
  ```
