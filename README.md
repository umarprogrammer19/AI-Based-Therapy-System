# CLI Todo App

A command-line todo application with priority management built with Python, Typer, and Rich.

## Features

- Create tasks with title, description, and priority (high/medium/low)
- List all tasks with filtering options
- Update existing tasks
- Mark tasks as completed
- Delete tasks
- Interactive menu system
- Persistent storage using JSON files

## Prerequisites

- Python 3.12+
- uv package manager

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   uv pip install typer rich pytest
   ```

## Usage

### Command Line Interface

The application provides several commands:

#### Create a task
```bash
python -m src.cli.main create --title "Task Title" --description "Task description" --priority high
```

#### List tasks
```bash
python -m src.cli.main list-tasks
```

#### Update a task
```bash
python -m src.cli.main update <task-id> --title "New Title" --completed true
```

#### Complete a task
```bash
python -m src.cli.main complete <task-id>
```

#### Delete a task
```bash
python -m src.cli.main delete <task-id>
```

#### Interactive menu
```bash
python -m src.cli.main menu
```

### Interactive Menu

The interactive menu provides a user-friendly way to manage tasks:
1. Create Task - Add new tasks with title, description, and priority
2. List Tasks - View all tasks with filtering options
3. Update Task - Modify existing tasks
4. Complete Task - Mark tasks as completed
5. Delete Task - Remove tasks
6. Exit - Quit the application

## Project Structure

```
src/
├── models/
│   └── task.py          # Task data model with priority, status, etc.
├── services/
│   └── task_service.py  # Task management logic (CRUD operations)
├── cli/
│   └── main.py          # Main CLI interface with Typer
└── lib/
    ├── storage.py       # File-based storage implementation
    └── logging_config.py # Logging configuration
```

## Testing

Run all tests:
```bash
python -m pytest
```

Run unit tests:
```bash
python -m pytest tests/unit/
```

Run contract tests:
```bash
python -m pytest tests/contract/
```

## Data Model

### Task
- `id`: Unique identifier (UUID)
- `title`: Task title (required, max 200 characters)
- `description`: Optional task description (max 1000 characters)
- `priority`: Priority level (high, medium, low)
- `completed`: Completion status (boolean)
- `created_at`: Timestamp when task was created
- `updated_at`: Timestamp when task was last updated

## Architecture

The application follows a clean architecture pattern:

- **Models**: Define the data structures (Task)
- **Services**: Contain business logic (TaskService)
- **CLI**: Handle user interface and commands
- **Lib**: Provide utility functions (Storage, Logging)

## Storage

Tasks are stored in a JSON file named `tasks.json` in the current directory. The storage system provides:

- Save tasks to file
- Load tasks from file
- Clear all tasks