# Design: Verify and Fix Subject Endpoints

## 1. Guiding Principles

- **Correctness:** The primary goal is to fix the bug and ensure all endpoints behave as expected.
- **Security:** Authorization checks must be correct and robust.
- **Minimalism:** Only change what is necessary to fix the bug.

## 2. Technical Architecture

The existing architecture will be maintained. The fix is localized to a single endpoint's logic.
The relevant files are in `apis/subjects/`.
- `4000000_subjects_POST.xs`
- `4000001_subjects_GET.xs`
- `4000002_subjects_by_id_GET.xs`
- `4000003_subjects_by_id_PATCH.xs` (to be modified)
- `4000004_subjects_by_id_DELETE.xs`

## 3. Data Model

No changes to the data model are required. The `subject` table schema will remain the same.

## 4. API Endpoints

- **`POST /subjects`**: No change.
- **`GET /subjects`**: No change.
- **`GET /subjects/{id}`**: No change.
- **`DELETE /subjects/{id}`**: No change.
- **`PATCH /subjects/{id}`**:
    - **File:** `apis/subjects/4000003_subjects_by_id_PATCH.xs`
    - **Change:** The precondition for the authorization check will be modified.
    - **Current (buggy) code:** `precondition ($subject.user_id == $auth.id)`
    - **Corrected code:** `precondition ($subject.user_id != $auth.id)`
    - This will ensure that if the subject's `user_id` does not match the authenticated user's `id`, an `accessdenied` error is thrown.

## 5. User Experience

The user experience will be improved as users will now be able to update their own subjects, which was previously broken. The API will behave as expected.
