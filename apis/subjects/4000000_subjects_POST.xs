query "subjects" verb=POST {
  api_group = "subjects"
  auth = true

  input {
    text name
    text? description
  }

  stack {
    db.add subject {
      created_at = "now"
      name = $input.name
      description = $input.description
      user_id = $auth.id
    } as $new_subject
  }

  response = $new_subject
  tags = []
}
