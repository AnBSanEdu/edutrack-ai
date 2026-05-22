query subjects verb=GET {
  api_group = "subjects"
  auth = "user"

  input {
    bool archived?=false
  }

  stack {
    db.query subject {
      where = $db.subject.user_id == $auth.id && $db.subject.archived == $input.archived
      return = {type: "list"}
      output = ["id", "created_at", "name", "description", "professor", "workload", "semester", "archived", "user_id"]
    } as $subjects
  }

  response = $subjects
}