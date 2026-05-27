// Atualizar uma tarefa específica do usuário autenticado (inclui marcar como concluída).
query academic_tasks_by_id verb=PATCH {
  api_group = "AcademicTasks"
  auth = "user"

  input {
    int id
    text? title
    text? description
    timestamp? due_date
    text? status
    text? priority
  }

  stack {
    // Verificar que a tarefa pertence ao usuário
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.id
    } as $task
  
    precondition ($task == null || $task.user_id != $auth.id) {
      error_type = "accessdenied"
      error = "Tarefa não encontrada ou sem permissão."
    }
  
    // Aplicar a atualização
    db.edit academic_tasks {
      field_name = "id"
      field_value = $input.id
      data = {
        title      : $input.title || $task.title
        description: $input.description || $task.description
        due_date   : $input.due_date || $task.due_date
        status     : $input.status || $task.status
        priority   : $input.priority || $task.priority
      }
    } as $updated_task
  }

  response = $updated_task
}