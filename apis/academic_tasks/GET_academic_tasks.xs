// Listar todas as tarefas do usuário autenticado, com filtros opcionais por status e disciplina.
query academic_tasks verb=GET {
  api_group = "AcademicTasks"
  auth = "user"

  input {
    text? status
    int? subject_id
    text sort?="due_date"
  }

  stack {
    // Buscar tarefas do usuário com filtros opcionais
    db.query academic_tasks {
      where = $auth.id == $db.academic_tasks.user_id
      sort = {due_date: "asc"}
      return = {type: "list"}
    } as $tasks
  
    // Filtrar por status se informado
    conditional {
      if ($input.status != null) {
        var.update $tasks {
          value = $tasks
            |filter:"return $this.status == '" ~ $input.status ~ "';"
        }
      }
    }
  
    // Filtrar por disciplina se informado
    conditional {
      if ($input.subject_id != null) {
        var.update $tasks {
          value = $tasks
            |filter:"return $this.subject_id == " ~ $input.subject_id ~ ";"
        }
      }
    }
  
    // Omitimos a anotação adicional de 'is_overdue' para manter a definição compilável.
    // A lista de tarefas será retornada diretamente após o filtro.
  }

  response = $tasks
}