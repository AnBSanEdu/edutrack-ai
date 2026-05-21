# Tasks: Verify and Fix Subject Endpoints

> A list of tasks to implement the change.

- [x] Task 1: Read the file `apis/subjects/4000003_subjects_by_id_PATCH.xs`.
- [x] Task 2: Modify the precondition in `apis/subjects/4000003_subjects_by_id_PATCH.xs` to fix the authorization bug.
    - Change `precondition ($subject.user_id == $auth.id)` to `precondition ($subject.user_id != $auth.id)`.
- [x] Task 3: Create a test file to verify the fix and the functionality of all `subjects` CRUD endpoints. The test file should be `testes_apis/patch_subject_by_id_tests.md`.
    - The test should include cases for:
        - A user successfully updating their own subject.
        - A user being blocked from updating another user's subject.
- [x] Task 4: Review existing tests in `testes_apis/` for the other subject endpoints and create them if they don't exist.
    - `get_subjects_tests.md`
    - `post_subjects_tests.md`
    - `get_subject_by_id_tests.md`
    - `delete_subject_by_id_tests.md`
