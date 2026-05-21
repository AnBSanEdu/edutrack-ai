# Proposal: Verify and Fix Subject Endpoints

## 1. The Big Picture

This change verifies the existing CRUD endpoints for `subjects` and fixes a bug in the `PATCH` endpoint to ensure correct authorization.

## 2. Problem

The `PATCH /subjects/{id}` endpoint has a bug in its access control logic. It incorrectly prevents the owner of a subject from updating it. While the user requested the creation of CRUD endpoints, they already exist, but one of them is faulty.

## 3. Goals

**Goals:**
- Verify that `POST`, `GET` (all), `GET` (by id), and `DELETE` endpoints for `subjects` work as expected and enforce ownership.
- Fix the bug in the `PATCH /subjects/{id}` endpoint to allow owners to update their subjects.
- Document the existing endpoints and the fix.

**Non-Goals:**
- Creating new endpoints from scratch.
- Changing the data model of `subjects`.

## 4. Proposed Solution

The solution involves three parts:
1.  **Review:** Analyze all existing endpoints in `apis/subjects/` to confirm their functionality.
2.  **Fix:** Correct the precondition in `apis/subjects/4000003_subjects_by_id_PATCH.xs` from `$subject.user_id == $auth.id` to `$subject.user_id != $auth.id` to correctly check for ownership.
3.  **Test:** Add tests for all endpoints to ensure they are working correctly and securely.
