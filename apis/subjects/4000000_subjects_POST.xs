query subjects verb=POST {
  api_group = "subjects"
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