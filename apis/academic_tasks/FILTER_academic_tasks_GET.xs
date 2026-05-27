query "academic-tasks/filter" verb=GET {
  api_group = "AcademicTasks"
  auth = "user"

  input {
    text[] status? filters=trim
  }

  stack {
    precondition ($input.status == "Pendente" || $input.status == "Em andamento" || $input.status == "Concluída") {
      error = "Status inválido. Escolha entre: Pendente, Em andamento ou Concluída."
    }
  
    db.query academic_tasks {
      where = $auth.id == $db.academic_tasks.user_id && $db.academic_tasks.status ==? $input.status
      return = {type: "list"}
    } as $tasks
  }

  response = {data: $tasks, success: true}
}