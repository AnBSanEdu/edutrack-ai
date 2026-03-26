## Context

Based on the proposal, we need to implement a system for users to manage their academic subjects. This requires a new database table and a set of API endpoints to interact with that data. The design will follow the existing project structure, which appears to be based on Xano, including database tables and RESTful API endpoints.

## Goals / Non-Goals

**Goals:**
- Define the schema for a new `subject` database table.
- Specify the API endpoints for full CRUD (Create, Read, Update, Delete) functionality for subjects.
- Ensure all API endpoints are protected and that users can only access or modify their own subjects.
- The design should be consistent with the existing Xano-based architecture.

**Non-Goals:**
- Implementation of the frontend UI for subject management.
- Creation of an admin-level interface for managing all subjects in the system. This design focuses solely on user-owned subjects.
- Complex automations beyond the basic CRUD functionality.

## Decisions

### 1. Database Schema
A new table named `subject` will be created with the following structure:

- **`id`**: (Integer) Primary Key, auto-incrementing.
- **`created_at`**: (Timestamp) Automatically set on creation.
- **`name`**: (Text) The name of the academic subject (e.g., "History 101"). Required.
- **`description`**: (Text) An optional, more detailed description of the subject.
- **`user_id`**: (Integer) A foreign key reference to the `user` table's `id` field, linking the subject to its owner. This field is required and will be indexed.

**Rationale**: This schema is simple, effective for the stated purpose, and includes the necessary `user_id` for ownership and access control, aligning with the proposal.

### 2. API Endpoints
A new API group named `subjects` will be created with the following endpoints. All endpoints require user authentication.

- **`POST /subjects`** - **Create Subject**
  - **Inputs**: `name` (text), `description` (text, optional).
  - **Logic**: Creates a new `subject` record, setting the `user_id` from the authenticated user's ID. Returns the newly created subject object.

- **`GET /subjects`** - **List User's Subjects**
  - **Logic**: Returns a list of all subjects where the `user_id` matches the authenticated user's ID. Supports pagination.

- **`GET /subjects/{id}`** - **Get Subject**
  - **Logic**: Retrieves a single `subject` record by its `id`. Before returning the record, it verifies that the `user_id` on the record matches the authenticated user's ID. If not, it returns a "Not Found" or "Forbidden" error.

- **`PATCH /subjects/{id}`** - **Update Subject**
  - **Inputs**: `name` (text, optional), `description` (text, optional).
  - **Logic**: First, retrieves the subject by `id` and verifies ownership (as in `GET /subjects/{id}`). If ownership is confirmed, it updates the provided fields.

- **`DELETE /subjects/{id}`** - **Delete Subject**
  - **Logic**: First, retrieves the subject by `id` and verifies ownership. If ownership is confirmed, it deletes the record.

**Rationale**: This RESTful API design is standard and provides a clean, intuitive interface for managing subject resources while embedding the necessary security and ownership checks.

### 3. Access Control
Ownership will be enforced at the API function level for every request that targets a specific resource (`GET`, `PATCH`, `DELETE` by id).

- A precondition/function step will be added at the beginning of each relevant API endpoint to fetch the subject record from the database.
- It will then compare the `subject.user_id` with the `auth.id` (ID of the authenticated user).
- If they do not match, the function will immediately stop execution and return an authorization error (e.g., HTTP 403 Forbidden or 404 Not Found to prevent data leakage).

**Rationale**: This approach ensures that data access is tightly controlled and prevents any user from accessing another user's data, which was a core requirement of the proposal. It reuses the pattern likely established in `role_based_access_control.xs`.

## Risks / Trade-offs

- **Risk**: No frontend is being built.
  - **Mitigation**: The API will be testable via API testing tools (like Postman or built-in Xano tools), ensuring its correctness before any frontend work begins.
- **Trade-off**: The current design doesn't support shared subjects between users. It uses a strict ownership model. This simplifies the initial implementation and security model but might need to be revisited if sharing becomes a requirement.
