// Excluir uma tarefa acadêmica do usuário autenticado.
query "academic_tasks/:id" verb=DELETE {
  api_group = "AcademicTasks"

  input {
    int id
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

    // Excluir a tarefa
    db.delete academic_tasks {
      id = $input.id
    }
  }

  response = {success: true, message: "Tarefa excluída com sucesso."}
}
