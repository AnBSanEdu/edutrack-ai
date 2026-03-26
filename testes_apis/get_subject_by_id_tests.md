# Test Cases for GET /subjects/{id}

This document outlines the test cases for the `GET /subjects/{id}` endpoint.

---

### Test Case 1: Successfully Retrieve an Owned Subject

- **Objective**: Verify that an authenticated user can retrieve a specific subject that they own.
- **Setup**:
  - Authenticate as User A and create a subject. Note the `id` of this subject.
- **Action**:
  - As User A, send a `GET` request to `/subjects/{id}`, where `{id}` is the ID of the subject created.
  - **Headers**: `Authorization: Bearer <user_a_auth_token>`
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - The returned JSON object should not be null.
    - The `id` in the response should match the `{id}` requested.
    - The `user_id` should match the ID of User A.

---

### Test Case 2: Attempt to Retrieve a Subject Owned by Another User

- **Objective**: Verify that a user cannot retrieve a subject owned by another user.
- **Setup**:
  - Authenticate as User B and create a subject. Note the `id` of this subject.
  - Authenticate as User A.
- **Action**:
  - As User A, send a `GET` request to `/subjects/{id}`, where `{id}` is the ID of the subject created by User B.
  - **Headers**: `Authorization: Bearer <user_a_auth_token>`
- **Assertions**:
  - **Status Code**: Expect HTTP `403 Forbidden` or `404 Not Found` (to prevent leaking information about the existence of resources).
  - **Response Body**: Should contain a relevant error message.

---

### Test Case 3: Attempt to Retrieve a Non-Existent Subject

- **Objective**: Verify that requesting a subject with an ID that does not exist results in an error.
- **Setup**:
  - Authenticate as any user.
- **Action**:
  - Send a `GET` request to `/subjects/999999` (where 999999 is an ID that is guaranteed not to exist).
  - **Headers**: `Authorization: Bearer <auth_token>`
- **Assertions**:
  - **Status Code**: Expect HTTP `404 Not Found`.

---

### Test Case 4: Unauthenticated Request

- **Objective**: Verify that an unauthenticated user cannot retrieve a subject.
- **Setup**:
  - A subject exists with a known ID.
  - No user is authenticated.
- **Action**:
  - Send a `GET` request to `/subjects/{id}` without an `Authorization` header.
- **Assertions**:
  - **Status Code**: Expect HTTP `401 Unauthorized`.
