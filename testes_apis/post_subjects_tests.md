# Test Cases for POST /subjects

This document outlines the test cases for the `POST /subjects` endpoint.

---

### Test Case 1: Successful Subject Creation

- **Objective**: Verify that an authenticated user can successfully create a new subject with all valid fields.
- **Setup**:
  - Authenticate as a standard user to obtain an auth token.
- **Action**:
  - Send a `POST` request to `/subjects`.
  - **Headers**: `Authorization: Bearer <auth_token>`
  - **Body**:
    ```json
    {
      "name": "Introduction to Psychology",
      "description": "A beginner's course on human behavior and mental processes."
    }
    ```
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - The returned JSON object should not be null.
    - `name` should be "Introduction to Psychology".
    - `description` should be "A beginner's course on human behavior and mental processes.".
    - `user_id` should match the ID of the authenticated user.
    - `id` and `created_at` should be present and have valid values.

---

### Test Case 2: Successful Creation with Required Fields Only

- **Objective**: Verify that a subject can be created with only the required `name` field.
- **Setup**:
  - Authenticate as a standard user.
- **Action**:
  - Send a `POST` request to `/subjects`.
  - **Headers**: `Authorization: Bearer <auth_token>`
  - **Body**:
    ```json
    {
      "name": "Calculus I"
    }
    ```
- **Assertions**:
  - **Status Code**: Expect HTTP `200 OK`.
  - **Response Body**:
    - `name` should be "Calculus I".
    - `description` should be `null` or not present.
    - `user_id` should match the ID of the authenticated user.

---

### Test Case 3: Missing Required Field (`name`)

- **Objective**: Verify that the request fails when the required `name` field is missing.
- **Setup**:
  - Authenticate as a standard user.
- **Action**:
  - Send a `POST` request to `/subjects`.
  - **Headers**: `Authorization: Bearer <auth_token>`
  - **Body**:
    ```json
    {
      "description": "This should fail."
    }
    ```
- **Assertions**:
  - **Status Code**: Expect HTTP `400 Bad Request` (or a similar client error for validation).
  - **Response Body**: Should contain an error message indicating that the `name` field is required.

---

### Test Case 4: Unauthenticated Request

- **Objective**: Verify that an unauthenticated user cannot create a subject.
- **Setup**:
  - No user is authenticated.
- **Action**:
  - Send a `POST` request to `/subjects` without an `Authorization` header.
  - **Body**:
    ```json
    {
      "name": "Unauthorized Test"
    }
    ```
- **Assertions**:
  - **Status Code**: Expect HTTP `401 Unauthorized`.
