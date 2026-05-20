table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now
    int user_id
    int subject_id
    text title
    text? description
    timestamp? due_date
    enum status? {
      values = ["pending", "in-progress", "completed"]
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "subject_id", op: "asc"}]}
  ]
}