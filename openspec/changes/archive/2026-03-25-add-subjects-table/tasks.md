## 1. Database Setup

- [x] 1.1 Create the `subject` table in the database with the following fields: `id` (Integer, PK), `created_at` (Timestamp), `name` (Text), `description` (Text), and `user_id` (Integer).
- [x] 1.2 Establish a foreign key relationship from `subject.user_id` to the `user.id` field.
- [x] 1.3 Add a database index to the `user_id` column on the `subject` table to optimize queries.

## 2. API Implementation

- [x] 2.1 Create a new API group named `subjects`.
- [x] 2.2 Develop the `POST /subjects` endpoint. It must take `name` and optional `description` as inputs and link the new record to the authenticated user's ID.
- [x] 2.3 Develop the `GET /subjects` endpoint to list all subjects owned by the authenticated user.
- [x] 2.4 Develop the `GET /subjects/{id}` endpoint to retrieve a single subject, ensuring the record belongs to the authenticated user.
- [x] 2.5 Develop the `PATCH /subjects/{id}` endpoint to update a subject, ensuring the record belongs to the authenticated user.
- [x] 2.6 Develop the `DELETE /subjects/{id}` endpoint to delete a subject, ensuring the record belongs to the authenticated user.

## 3. Testing and Validation

- [x] 3.1 Create and run tests for the `POST /subjects` endpoint to verify subject creation and proper user assignment.
- [x] 3.2 Create and run tests for the `GET /subjects` endpoint to verify that only user-owned subjects are returned.
- [x] 3.3 Create and run tests for the `GET /subjects/{id}` endpoint, including success cases and failure cases for incorrect ownership.
- [x] 3.4 Create and run tests for the `PATCH /subjects/{id}` endpoint, including success cases and failure cases for incorrect ownership.
- [x] 3.5 Create and run tests for the `DELETE /subjects/{id}` endpoint, including success cases and failure cases for incorrect ownership.
