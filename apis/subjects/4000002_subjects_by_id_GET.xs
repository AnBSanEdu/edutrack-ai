query "subjects/{id}" verb=GET {
  api_group = "subjects"
  auth = "user"

  input {
    int id
  }

  stack {
    db.get subject {
      field_name = "id"
      field_value = $input.id
      output = ["id", "created_at", "name", "description", "professor", "workload", "semester", "archived", "user_id"]
    } as $subject
  
    precondition ($subject == null) {
      error_type = "notfound"
      error = "Subject not found."
    }
  
    precondition ($subject.user_id != $auth.id) {
      error_type = "accessdenied"
      error = "You do not have permission to access this subject."
    }
  }

  response = $subject
}