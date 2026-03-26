# Test Cases for GET /subjects

This document outlines the test cases for the `GET /subjects` endpoint.

---

### Test Case 1: Successfully Retrieve Owned Subjects

- **Objective**: Verify that an authenticated user can retrieve a list of all subjects they own.
- **Setup**:
  - Authenticate as User A.
  - Create two subjects ("Subject 1", "Subject 2") as User A.
  - Authenticate as User B and create one subject ("Subject 3").
- **Action**:
  - As User A, send a `GET` request to `/subjects`.
  - **Headers**: `Authorization: Bearer <user_a_auth_token>`
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - The response should be a JSON array.
    - The array should contain exactly two items.
    - The names of the subjects in the array should be "Subject 1" and "Subject 2".
    - The array must not contain "Subject 3".

---

### Test Case 2: Retrieve Subjects When User Has None

- **Objective**: Verify that the endpoint returns an empty list for a user who has not created any subjects.
- **Setup**:
  - Authenticate as a new user, User C, who has no subjects.
- **Action**:
  - As User C, send a `GET` request to `/subjects`.
  - **Headers**: `Authorization: Bearer <user_c_auth_token>`
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - The response should be an empty JSON array (`[]`).

---

### Test Case 3: Unauthenticated Request

- **Objective**: Verify that an unauthenticated user cannot retrieve subjects.
- **Setup**:
  - No user is authenticated.
- **Action**:
  - Send a `GET` request to `/subjects` without an `Authorization` header.
- **Assertions**:
  - **Status Code**: Expect HTTP `401 Unauthorized`.
