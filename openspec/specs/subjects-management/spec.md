## ADDED Requirements

### Requirement: User can create a subject
The system SHALL allow an authenticated user to create a new academic subject. The subject MUST be associated with the user who created it.

#### Scenario: Successful creation with all fields
- **WHEN** an authenticated user submits a request to create a subject with a name and a description.
- **THEN** the system SHALL create a new subject record with the provided name and description, linked to the user's ID.
- **AND** the system SHALL return the newly created subject object.

#### Scenario: Successful creation with only required fields
- **WHEN** an authenticated user submits a request to create a subject with only a name.
- **THEN** the system SHALL create a new subject record with the provided name and a null description, linked to the user's ID.
- **AND** the system SHALL return the newly created subject object.

#### Scenario: Creation without a name
- **WHEN** a user attempts to create a subject without a name.
- **THEN** the system SHALL reject the request with a validation error.

#### Scenario: Unauthenticated user attempts creation
- **WHEN** an unauthenticated user attempts to create a subject.
- **THEN** the system SHALL reject the request with an authentication error.

### Requirement: User can retrieve their subjects
The system SHALL allow an authenticated user to retrieve subjects they own.

#### Scenario: Retrieve all owned subjects
- **WHEN** an authenticated user requests their list of subjects.
- **THEN** the system SHALL return a list containing only the subjects owned by that user.

#### Scenario: Retrieve a specific owned subject
- **WHEN** an authenticated user requests a subject by an ID that they own.
- **THEN** the system SHALL return the corresponding subject object.

#### Scenario: Attempt to retrieve a subject owned by another user
- **WHEN** an authenticated user requests a subject by an ID owned by another user.
- **THEN** the system SHALL return a "Not Found" or "Forbidden" error.

#### Scenario: Unauthenticated user attempts retrieval
- **WHEN** an unauthenticated user attempts to retrieve any subject.
- **THEN** the system SHALL reject the request with an authentication error.

### Requirement: User can update their subject
The system SHALL allow an authenticated user to update the details of a subject they own.

#### Scenario: Successful update
- **WHEN** an authenticated user submits an update to the name or description of a subject they own.
- **THEN** the system SHALL update the subject record with the new information.
- **AND** the system SHALL return the updated subject object.

#### Scenario: Attempt to update a subject owned by another user
- **WHEN** an authenticated user attempts to update a subject owned by another user.
- **THEN** the system SHALL return a "Not Found" or "Forbidden" error.

#### Scenario: Unauthenticated user attempts update
- **WHEN** an unauthenticated user attempts to update a subject.
- **THEN** the system SHALL reject the request with an authentication error.

### Requirement: User can delete their subject
The system SHALL allow an authenticated user to delete a subject they own.

#### Scenario: Successful deletion
- **WHEN** an authenticated user requests to delete a subject they own.
- **THEN** the system SHALL delete the subject record.
- **AND** the system SHALL return a success confirmation.

#### Scenario: Attempt to delete a subject owned by another user
- **WHEN** an authenticated user attempts to delete a subject owned by another user.
- **THEN** the system SHALL return a "Not Found" or "Forbidden" error.

#### Scenario: Unauthenticated user attempts deletion
- **WHEN** an unauthenticated user attempts to delete a subject.
- **THEN** the system SHALL reject the request with an authentication error.
