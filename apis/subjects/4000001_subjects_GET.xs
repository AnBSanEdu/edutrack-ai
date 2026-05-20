query subjects verb=GET {
  api_group = "subjects"
  auth = "user"

  input {
  }

  stack {
    db.query subject {
      where = $db.subject.user_id == $auth.id
      return = {type: "list"}
      output = ["id", "created_at", "name", "description", "user_id"]
    } as $subjects
  }

  response = $subjects
}