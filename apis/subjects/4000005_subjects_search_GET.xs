query "subjects/search/" verb=GET {
  api_group = "Subjects"
  auth = "user"

  input {
    text? name
    bool? has_overdue_tasks
  }

  stack {
    // 1. Initial search
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $subjects

    // 2. Filter by name if provided
    conditional {
      if ($input.name != null) {
        var.update $subjects {
          value = $subjects|filter:"return $this.name contains '" ~ $input.name ~ "';"
        }
      }
    }

    // 3. Filter by overdue tasks if requested
    conditional {
      if ($input.has_overdue_tasks == true) {
        var $overdue_subjects {
          value = []
        }
        foreach ($subjects) {
          each as $subject {
            db.query academic_tasks {
              where = $db.academic_tasks.subject_id == $subject.id && $db.academic_tasks.due_date < "now" && $db.academic_tasks.status != "Concluída"
              return = { type: "count" }
            } as $overdue_count

            conditional {
              if ($overdue_count > 0) {
                var.update $overdue_subjects {
                  value = $overdue_subjects|push:$subject
                }
              }
            }
          }
        }
        var.update $subjects {
          value = $overdue_subjects
        }
      }
    }
  }

  response = {
    success: true,
    data: $subjects
  }
}
