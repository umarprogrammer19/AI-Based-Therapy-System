---
description: "Task list for CLI Todo App implementation"
---

# Tasks: CLI Todo App

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The feature specification includes testing requirements - tests will be included as per constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/ and tests/
- [X] T002 Initialize Python 3.12+ project with typer, rich, pytest dependencies using uv
- [X] T003 [P] Create pyproject.toml with proper dependencies and configuration

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create Task data model in src/models/task.py with all required fields and validation
- [X] T005 Create file-based storage implementation in src/lib/storage.py for JSON persistence
- [X] T006 Create TaskService in src/services/task_service.py with CRUD operations
- [X] T007 Create priority enum in src/models/task.py for high/medium/low values
- [X] T008 Configure logging and error handling infrastructure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create Task with Priority (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new tasks with title, description, and priority levels (high/medium/low)

**Independent Test**: User can successfully add a new task with title, description, and priority level, which is then stored and can be viewed later.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T009 [P] [US1] Contract test for create_task operation in tests/contract/test_task_contracts.py
- [X] T010 [P] [US1] Unit test for Task model validation in tests/unit/test_task.py

### Implementation for User Story 1

- [X] T011 [US1] Create CLI command for task creation in src/cli/main.py
- [X] T012 [US1] Implement create_task functionality in TaskService
- [X] T013 [US1] Add input validation for task creation parameters
- [X] T014 [US1] Implement storage persistence for new tasks
- [X] T015 [US1] Add user feedback for successful task creation

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View and List Tasks (Priority: P1)

**Goal**: Enable users to view all their tasks in a formatted list with priority indicators and completion status

**Independent Test**: User can view all tasks in a formatted list showing title, priority level, completion status, and other relevant details.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T016 [P] [US2] Contract test for list_tasks operation in tests/contract/test_task_contracts.py
- [ ] T017 [P] [US2] Integration test for task listing in tests/integration/test_cli.py

### Implementation for User Story 2

- [ ] T018 [US2] Create CLI command for task listing in src/cli/main.py
- [ ] T019 [US2] Implement list_tasks functionality in TaskService
- [ ] T020 [US2] Format task display with Rich for priority indicators
- [ ] T021 [US2] Add filtering options for completed/incomplete tasks
- [ ] T022 [US2] Add sorting options by priority, creation date, or title

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update and Complete Tasks (Priority: P1)

**Goal**: Enable users to update their tasks and mark them as complete to track progress

**Independent Test**: User can modify existing tasks and mark them as complete, with changes being saved and reflected in the task list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T023 [P] [US3] Contract test for update_task and complete_task operations in tests/contract/test_task_contracts.py
- [ ] T024 [P] [US3] Unit test for task update validation in tests/unit/test_task_service.py

### Implementation for User Story 3

- [ ] T025 [US3] Create CLI command for task updating in src/cli/main.py
- [ ] T026 [US3] Create CLI command for marking tasks complete in src/cli/main.py
- [ ] T027 [US3] Implement update_task functionality in TaskService
- [ ] T028 [US3] Implement complete_task functionality in TaskService
- [ ] T029 [US3] Add validation to prevent operations on non-existent tasks

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P2)

**Goal**: Enable users to delete tasks they no longer need to keep their todo list clean

**Independent Test**: User can remove tasks from the list, with the deletion being permanent and reflected in the task list.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T030 [P] [US4] Contract test for delete_task operation in tests/contract/test_task_contracts.py
- [ ] T031 [P] [US4] Integration test for task deletion in tests/integration/test_cli.py

### Implementation for User Story 4

- [ ] T032 [US4] Create CLI command for task deletion in src/cli/main.py
- [ ] T033 [US4] Implement delete_task functionality in TaskService
- [ ] T034 [US4] Add confirmation prompt before deletion
- [ ] T035 [US4] Add user feedback for successful deletion

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: User Story 5 - Continuous Interactive Menu (Priority: P1)

**Goal**: Provide an interactive menu system that runs continuously until user chooses to exit

**Independent Test**: User can navigate through different operations (create, read, update, delete) continuously until choosing to exit the application.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T036 [P] [US5] Integration test for main menu flow in tests/integration/test_cli.py
- [ ] T037 [P] [US5] Unit test for menu navigation logic in tests/unit/test_cli.py

### Implementation for User Story 5

- [ ] T038 [US5] Implement main menu loop in src/cli/main.py
- [ ] T039 [US5] Add menu navigation options for all task operations
- [ ] T040 [US5] Implement graceful exit functionality
- [ ] T041 [US5] Add error handling for invalid user inputs
- [ ] T042 [US5] Format menu display with Rich for better UX

**Checkpoint**: All user stories should now be fully integrated and functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T043 [P] Add comprehensive documentation in README.md
- [ ] T044 Add error handling for edge cases (empty task lists, invalid IDs, etc.)
- [ ] T045 [P] Add additional unit tests in tests/unit/
- [ ] T046 Performance optimization for large task lists
- [ ] T047 Security hardening for file operations
- [ ] T048 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Integrates with all other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for create_task operation in tests/contract/test_task_contracts.py"
Task: "Unit test for Task model validation in tests/unit/test_task.py"

# Launch all models for User Story 1 together:
Task: "Create CLI command for task creation in src/cli/main.py"
Task: "Implement create_task functionality in TaskService"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence