query subjects verb=POST {
  api_group = "Subjects"
  auth = "user"

  input {
    text name
    text? description
    text? professor
    text? workload
    text? semester
    bool archived?=false
  }

  stack {
    db.query subjects {
      where = $db.subjects.name == $input.name && $db.subjects.professor == $input.professor && $db.subjects.user_id == $auth.id
      return = {type: "single"}
    } as $existing

    precondition ($existing == null) {
      error_type = "inputerror"
      error = "Você já possui uma disciplina cadastrada com este nome e professor."
    }

    db.add subjects {
      data = {
        created_at : "now"
        name       : $input.name
        description: $input.description
        professor  : $input.professor
        workload   : $input.workload
        semester   : $input.semester
        archived   : $input.archived
        user_id    : $auth.id
      }
    } as $new_subject
  }

  response = $new_subject
}
