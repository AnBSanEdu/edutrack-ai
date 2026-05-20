query subjects verb=POST {
  api_group = "subjects"
  auth = "user"

  input {
    text name
    text? description
  }

  stack {
    db.add subjects {
      data = {
        created_at : "now"
        name       : $input.name
        description: $input.description
        user_id    : $auth.id
      }
    } as $new_subject
  }

  response = $new_subject
}