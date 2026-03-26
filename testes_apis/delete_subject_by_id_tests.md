# Test Cases for DELETE /subjects/{id}

This document outlines the test cases for the `DELETE /subjects/{id}` endpoint.

---

### Test Case 1: Successfully Delete an Owned Subject

- **Objective**: Verify that an authenticated user can delete a subject they own.
- **Setup**:
  - Authenticate as User A and create a subject. Note the `id`.
- **Action**:
  - As User A, send a `DELETE` request to `/subjects/{id}`.
  - **Headers**: `Authorization: Bearer <user_a_auth_token>`
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK` or `204 No Content`.
  - **Response Body**: The response body might be empty or contain a success message.
  - **Database Verification**:
    - Attempt to `GET /subjects/{id}` for the deleted subject ID. This should result in a `404 Not Found`.
    - Query the database directly to confirm the record has been removed.

---

### Test Case 2: Attempt to Delete a Subject Owned by Another User

- **Objective**: Verify that a user cannot delete a subject owned by another user.
- **Setup**:
  - Authenticate as User B and create a subject. Note the `id`.
  - Authenticate as User A.
- **Action**:
  - As User A, send a `DELETE` request to `/subjects/{id}`, where `{id}` is for the subject owned by User B.
  - **Headers**: `Authorization: Bearer <user_a_auth_token>`
- **Assertions**:
  - **Status Code**: Expect HTTP `403 Forbidden` or `404 Not Found`.
  - **Database Verification**: The subject owned by User B should still exist in the database.

---

### Test Case 3: Attempt to Delete a Non-Existent Subject

- **Objective**: Verify that attempting to delete a non-existent subject results in an error.
- **Setup**:
  - Authenticate as any user.
- **Action**:
  - Send a `DELETE` request to `/subjects/999999`.
  - **Headers**: `Authorization: Bearer <auth_token>`
- **Assertions**:
  - **Status Code**: Expect HTTP `404 Not Found`.

---

### Test Case 4: Unauthenticated Request

- **Objective**: Verify that an unauthenticated user cannot delete a subject.
- **Setup**:
  - A subject exists with a known ID.
- **Action**:
  - Send a `DELETE` request to `/subjects/{id}` without an `Authorization` header.
- **Assertions**:
  - **Status Code**: Expect HTTP `401 Unauthorized`.
