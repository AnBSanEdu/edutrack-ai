query "subjects" verb=GET {
  api_group = "subjects"
  auth = true

  stack {
    db.query subject {
      where = $db.subject.user_id == $auth.id
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
  tags = []
}
