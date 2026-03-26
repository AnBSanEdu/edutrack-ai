query "subjects/{id}" verb=PATCH {
  api_group = "subjects"
  auth = true

  input {
    int id from=path
    text? name
    text? description
  }

  stack {
    db.get subject {
      field_name = "id"
      field_value = $input.id
    } as $subject

    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "You do not have permission to modify this subject."
    }

    db.edit subject {
      id = $input.id
      name = $input.name
      description = $input.description
    } as $updated_subject
  }

  response = $updated_subject
  tags = []
}
