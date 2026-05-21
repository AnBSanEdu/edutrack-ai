query "subjects/search" verb=GET {
  api_group = "subjects"
  auth = "user"

  input {
    text? name
    bool? has_overdue_tasks
  }

  stack {
    // 1. Busca inicial
    db.query subject {
      where = $db.subject.user_id == $auth.id
      return = {type: "list"}
    } as $subjects

    // 2. Atualização da variável usando a sintaxe correta 'var'
    if ($input.name != null) {
      var $subjects {
        value = $subjects|filter_match_ci:"name",$input.name
      }
    }

    // 3. Lógica para tarefas atrasadas
    if ($input.has_overdue_tasks == true) {
      // Aqui você deve usar uma função de manipulação de array ou filtro nativo
      var $subjects {
        value = $subjects|filter_array_by_overdue_tasks
      }
    }
  }

  // No bloco response, use ':' para objetos JSON
  response: {
    success: true,
    data: $subjects
  }
}
