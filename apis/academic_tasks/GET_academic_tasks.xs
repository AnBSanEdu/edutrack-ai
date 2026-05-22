// Listar todas as tarefas do usuário autenticado, com filtros opcionais por status e disciplina.
query "academic_tasks" verb=GET {
  api_group = "AcademicTasks"

  input {
    text?   status
    int?    subject_id
    text    sort?="due_date"
  }

  stack {
    // Obter o usuário autenticado
    auth.getUserRecord {} as $me

    // Buscar tarefas do usuário com filtros opcionais
    db.query academic_tasks {
      where {
        user_id == $me.id
        // Filtro de status (aplicado somente se informado)
        if ($input.status != null) {
          status == $input.status
        }
        // Filtro de disciplina (aplicado somente se informado)
        if ($input.subject_id != null) {
          subject_id == $input.subject_id
        }
      }
      sort {
        field = $input.sort
        op    = "asc"
      }
      output = [
        "id"
        "created_at"
        "subject_id"
        "title"
        "description"
        "due_date"
        "status"
        "priority"
      ]
    } as $tasks
  }

  response = $tasks
}
