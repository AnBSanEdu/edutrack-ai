
# Design Técnico: Lançamento de Notas

## 1. Estrutura de Dados

### Tabela: `academic_tasks`

Esta tabela irá armazenar as atividades criadas pelos professores.

- **Arquivo:** `tables/academic_tasks.xs`
- **Schema:**
  ```xanoscript
  table academic_tasks {
    text name;
    text description?;
    int subject_id; // FK para a tabela 'subject'
    datetime due_date?;
  }
  ```

### Tabela: `activity_grades`

Esta tabela associará um aluno, uma atividade e uma nota.

- **Arquivo:** `tables/activity_grades.xs`
- **Schema:**
  ```xanoscript
  table activity_grades {
    int task_id; // FK para a tabela 'academic_tasks'
    int student_id; // FK para a tabela 'user'
    int teacher_id; // FK para a tabela 'user' (quem lançou a nota)
    double grade;
    text comments?;
  }
  ```

## 2. API Endpoint

### Endpoint: `POST /activity_grades`

Este endpoint será usado para que um professor possa lançar uma nota.

- **Arquivo:** `apis/grades/post_activity_grade.xs`
- **Endpoint:** `POST /api/activity_grades`
- **Autorização:** Requer autenticação e que o usuário tenha a role de 'teacher'. A lógica de verificação de role será implementada usando o RBAC do sistema.

#### Request Body

```json
{
  "task_id": 1,
  "student_id": 123,
  "grade": 95.5,
  "comments": "Ótimo trabalho!"
}
```

#### Lógica de Negócio

1.  Validar os dados de entrada (`task_id`, `student_id`, `grade`).
2.  Verificar se o `auth.id` (usuário autenticado) possui a role 'teacher'.
3.  Verificar se `task_id` e `student_id` existem.
4.  Criar um novo registro na tabela `activity_grades` com os dados fornecidos e o `teacher_id` sendo o `auth.id`.
5.  Retornar o registro criado com status 201.
