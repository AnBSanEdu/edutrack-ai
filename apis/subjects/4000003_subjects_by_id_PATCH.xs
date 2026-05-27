query "subjects/{id}" verb=PATCH {
  api_group = "Subjects"
  auth = "user"

  input {
    int id
    text? name
    text? description
    text? professor
    text? workload
    text? semester
    bool? archived
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
      error = "You do not have permission to modify this subject."
    }
  
    db.edit subjects {
      field_name = "id"
      field_value = $input.id
      data = {
        name       : $input.name || $subject.name
        description: $input.description || $subject.description
        professor  : $input.professor || $subject.professor
        workload   : $input.workload || $subject.workload
        semester   : $input.semester || $subject.semester
        archived   : $subject.archived
      }
    } as $updated_subject
  }

  response = $updated_subject
}