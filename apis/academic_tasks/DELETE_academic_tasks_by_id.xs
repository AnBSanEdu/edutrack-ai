// Excluir uma tarefa acadêmica do usuário autenticado.
query "academic_tasks/id" verb=DELETE {
  api_group = "AcademicTasks"
  auth = "user"

  input {
    int id
  }

  stack {
    // Verificar que a tarefa pertence ao usuário
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.id
      output = ["id", "user_id"]
    } as $task
  
    precondition ($task != null && $task.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Tarefa não encontrada ou sem permissão."
    }
  
    // Excluir a tarefa
    db.del academic_tasks {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = {
    success: true
    message: "Tarefa excluída com sucesso."
  }
}