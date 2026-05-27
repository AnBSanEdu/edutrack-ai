query subjects verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    bool archived?=false
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id && $db.subjects.archived == $input.archived
      return = {type: "list"}
      output = ["id", "created_at", "name", "description", "professor", "workload", "semester", "archived", "user_id"]
    } as $subjects
  }

  response = $subjects
}