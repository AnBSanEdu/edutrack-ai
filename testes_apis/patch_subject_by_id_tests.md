# Test Cases for PATCH /subjects/{id}

This document outlines the test cases for the `PATCH /subjects/{id}` endpoint.

---

### Test Case 1: Successfully Update an Owned Subject

- **Objective**: Verify that an authenticated user can update the `name` and `description` of a subject they own.
- **Setup**:
  - Authenticate as User A and create a subject with name "Old Name". Note the `id`.
- **Action**:
  - As User A, send a `PATCH` request to `/subjects/{id}`.
  - **Headers**: `Authorization: Bearer <user_a_auth_token>`
  - **Body**:
    ```json
    {
      "name": "New Name",
      "description": "Updated description."
    }
    ```
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - `id` should match the updated subject's ID.
    - `name` should be "New Name".
    - `description` should be "Updated description.".
  - **Database Verification**: Query the database directly to confirm the record was updated.

---

### Test Case 2: Attempt to Update a Subject Owned by Another User

- **Objective**: Verify that a user cannot update a subject owned by another user.
- **Setup**:
  - Authenticate as User B and create a subject. Note the `id`.
  - Authenticate as User A.
- **Action**:
  - As User A, send a `PATCH` request to `/subjects/{id}`, where `{id}` is for the subject owned by User B.
  - **Headers**: `Authorization: Bearer <user_a_auth_token>`
  - **Body**:
    ```json
    {
      "name": "This should fail"
    }
    ```
- **Assertions**:
  - **Status Code**: Expect HTTP `403 Forbidden` or `404 Not Found`.

---

### Test Case 3: Attempt to Update a Non-Existent Subject

- **Objective**: Verify that attempting to update a non-existent subject results in an error.
- **Setup**:
  - Authenticate as any user.
- **Action**:
  - Send a `PATCH` request to `/subjects/999999`.
  - **Headers**: `Authorization: Bearer <auth_token>`
  - **Body**:
    ```json
    {
      "name": "This should fail"
    }
    ```
- **Assertions**:
  - **Status Code**: Expect HTTP `404 Not Found`.

---

### Test Case 4: Unauthenticated Request

- **Objective**: Verify that an unauthenticated user cannot update a subject.
- **Setup**:
  - A subject exists with a known ID.
- **Action**:
  - Send a `PATCH` request to `/subjects/{id}` without an `Authorization` header.
- **Assertions**:
  - **Status Code**: Expect HTTP `401 Unauthorized`.
