query "subjects/{id}" verb=DELETE {
  api_group = "subjects"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get subject {
      field_name = "id"
      field_value = $input.id
      output = ["id", "user_id"]
    } as $subject

    precondition ($subject == null) {
      error_type = "notfound"
      error = "Subject not found."
    }

    precondition ($subject.user_id != $auth.id) {
      error_type = "accessdenied"
      error = "You do not have permission to delete this subject."
    }

    db.delete {
      table = "subject"
      field_name = "id"
      field_value = $input.id
    } as $deleted_subject
  }

  response = $deleted_subject
}
