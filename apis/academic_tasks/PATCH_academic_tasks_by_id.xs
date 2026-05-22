// Atualizar uma tarefa específica do usuário autenticado (inclui marcar como concluída).
query "academic_tasks/:id" verb=PATCH {
  api_group = "AcademicTasks"

  input {
    int     id
    text?   title
    text?   description
    timestamp? due_date
    text?   status
    text?   priority
  }

  stack {
    // Obter o usuário autenticado
    auth.getUserRecord {} as $me

    // Verificar que a tarefa pertence ao usuário
    db.get academic_tasks {
      field_name  = "id"
      field_value = $input.id
      output      = ["id", "user_id"]
    } as $task

    precondition ($task != null && $task.user_id == $me.id) {
      error_type = "accessdenied"
      error      = "Tarefa não encontrada ou sem permissão."
    }

    // Montar payload com somente os campos informados
    var payload = {}

    if ($input.title != null) {
      var payload = array.merge($payload, {title: $input.title})
    }

    if ($input.description != null) {
      var payload = array.merge($payload, {description: $input.description})
    }

    if ($input.due_date != null) {
      var payload = array.merge($payload, {due_date: $input.due_date})
    }

    if ($input.status != null) {
      var payload = array.merge($payload, {status: $input.status})
    }

    if ($input.priority != null) {
      var payload = array.merge($payload, {priority: $input.priority})
    }

    // Aplicar a atualização
    db.edit academic_tasks {
      id   = $input.id
      data = $payload
    } as $updated_task
  }

  response = $updated_task
}
