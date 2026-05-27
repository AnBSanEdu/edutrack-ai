query "subjects/:id" verb=DELETE {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.id
      output = ["id", "user_id"]
    } as $subject
  
    precondition ($subject != null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    precondition ($subject.user_id == $auth.id) {
      error_type = "accessdenied"
      error = "You do not have permission to delete this subject."
    }
  
    db.del "subjects" {
      field_name = "id"
      field_value = $input.id
    }
  }

  response = $subject
}