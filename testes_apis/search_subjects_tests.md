# Test Cases for GET /subjects/search

This document outlines the test cases for the `GET /subjects/search` endpoint.

---

### Test Case 1: Search by Name (Successful)

- **Objective**: Verify that a user can successfully search for their subjects by name.
- **Setup**:
  - Authenticate as User A.
  - Create two subjects: "História do Brasil" and "Geografia do Brasil".
- **Action**:
  - As User A, send a `GET` request to `/subjects/search?name=Brasil`.
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - The response should be a JSON array containing two subjects.
    - Both subjects should have "Brasil" in their names.

---

### Test Case 2: Search by Name (No Results)

- **Objective**: Verify that an empty list is returned when no subjects match the search term.
- **Setup**:
  - Authenticate as User A.
  - Create a subject: "História do Brasil".
- **Action**:
  - As User A, send a `GET` request to `/subjects/search?name=Argentina`.
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - The response should be an empty JSON array (`[]`).

---

### Test Case 3: Filter by Overdue Tasks (Successful)

- **Objective**: Verify that a user can filter subjects to show only those with overdue tasks.
- **Setup**:
  - Authenticate as User A.
  - Create a subject "Matemática" and associate an overdue `academic_task` to it.
  - Create a subject "Português" with no overdue tasks.
- **Action**:
  - As User A, send a `GET` request to `/subjects/search?has_overdue_tasks=true`.
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - The response should be a JSON array containing one subject.
    - The subject's name should be "Matemática".

---

### Test Case 4: Filter by Overdue Tasks (No Results)

- **Objective**: Verify that an empty list is returned when no subjects have overdue tasks.
- **Setup**:
  - Authenticate as User A.
  - Create two subjects, neither with overdue tasks.
- **Action**:
  - As User A, send a `GET` request to `/subjects/search?has_overdue_tasks=true`.
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - The response should be an empty JSON array (`[]`).

---

### Test Case 5: Search by Name and Filter by Overdue Tasks

- **Objective**: Verify that both `name` and `has_overdue_tasks` filters can be applied together.
- **Setup**:
  - Authenticate as User A.
  - Create "Cálculo I" with an overdue task.
  - Create "Cálculo II" with no overdue tasks.
  - Create "Álgebra Linear" with an overdue task.
- **Action**:
  - As User A, send a `GET` request to `/subjects/search?name=Cálculo&has_overdue_tasks=true`.
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - The response should be a JSON array containing one subject.
    - The subject's name should be "Cálculo I".

---

### Test Case 6: No Filters Applied

- **Objective**: Verify that all of the user's subjects are returned when no filters are applied.
- **Setup**:
  - Authenticate as User A and create three subjects.
- **Action**:
  - As User A, send a `GET` request to `/subjects/search`.
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - The response should be a JSON array containing all three subjects created by User A.

---

### Test Case 7: Unauthenticated Request

- **Objective**: Verify that an unauthenticated user cannot access the search endpoint.
- **Action**:
  - Send a `GET` request to `/subjects/search` without an `Authorization` header.
- **Assertions**:
  - **Status Code**: Expect HTTP `401 Unauthorized`.
