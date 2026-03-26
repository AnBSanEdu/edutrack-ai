## Why

This change introduces the ability for users to manage their academic subjects. It establishes a foundational data model for subjects, enabling ownership, access control, and a base for future academic-related automations and features.

## What Changes

- A new database table, `subjects`, will be created to store academic discipline information.
- API endpoints will be developed to allow authenticated users to perform CRUD (Create, Read, Update, Delete) operations on their own subjects.
- Each subject entry will be directly linked to a `user_id` to enforce data ownership and privacy.

## Capabilities

### New Capabilities
- `subjects-management`: Manages the lifecycle of academic subjects, including creation, retrieval, updates, and deletion, with user-based ownership.

### Modified Capabilities
<!-- No existing capabilities are being modified. -->

## Impact

- **Database**: A new `subjects` table will be added to the database schema.
- **API**: A new set of API endpoints will be introduced (e.g., under `/subjects`) to handle the new functionality.
- **Frontend**: Will require new UI components and services to interact with the new `subjects` API.
