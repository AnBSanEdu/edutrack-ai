query "subjects/{id}" verb=PATCH {
  api_group = "subjects"
  auth = "user"

  input {
    int id
    text? name
    text? description
  }

  stack {
    db.get subject {
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
      error = "You do not have permission to modify this subject."
    }
  
    util.get_all_input as $inputs
    db.patch subject {
      field_name = "id"
      field_value = $input.id
      data = $inputs|filter_empty_text:""
    } as $updated_subject
  }

  response = $updated_subject
}