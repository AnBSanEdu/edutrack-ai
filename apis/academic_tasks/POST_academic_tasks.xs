// Criar uma nova tarefa acadêmica vinculada ao usuário autenticado e a uma disciplina.
query academic_tasks verb=POST {
  api_group = "AcademicTasks"
  auth = "user"

  input {
    int subject_id
    text title
    text? description
    timestamp? due_date
    text status?=pending
    text priority?=medium
  }

  stack {
    // Garantir que o usuário está autenticado
    // Verificar que a disciplina pertence ao usuário
    db.get "" {
      field_name = "id"
      field_value = $input.subject_id
      output = ["id", "user_id"]
    } as $subject
  
    precondition ($subject != null && $subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "Disciplina não encontrada ou sem permissão."
    }
  
    // Criar a tarefa
    db.add academic_tasks {
      data = {
        user_id    : $auth.id
        subject_id : $input.subject_id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status
        priority   : $input.priority
      }
    } as $new_task
  }

  response = $new_task
}