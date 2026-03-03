# Project Management CLI Tool

A Python command-line application that lets administrators manage users, projects, and tasks from the terminal. Data is automatically saved between sessions using JSON file storage.


---

## Project Structure

```
project_manager/
│
├── main.py              Entry point — run all commands from here
├── Pipfile              Pipenv dependency manager
├── requirements.txt      pip dependency list
│
├── models/              Class definitions 
│   ├── __init__.py
│   ├── user.py          Person base class + User class 
│   ├── project.py       Project class
│   └── task.py          Task class
│
├── utils/               Helper/utility functions
│   ├── __init__.py
│   ├── file_io.py       Save and load data as JSON
│   └── helpers.py       Table display, search, date validation
│
├── data/                Auto-created on first run
│   └── data.json        All persisted data lives here
│
└── tests/               Unit tests
    ├── test_models.py   Tests for User, Project, Task classes
    └── test_cli.py      Tests for CLI handler functions
```

---

##  Setup Instructions

### 1. Check your Python version (must be 3.10 or higher)

```bash
python --version
```

### 2. Clone the repository

```bash
git clone 
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify the install worked

```bash
python3 -c "import tabulate; import dateutil; print('All packages installed!')"
```

---

## How to Run CLI Commands

All commands follow this pattern:

```
python main.py <command> [options]
```

To see help for any command, add `--help`:

```bash
python main.py --help
python main.py add-project --help
```

---

### Users

**Add a new user:**
```bash
python main.py add-user --name "Alex" --email "alex@email.com"
```

**List all users:**
```bash
python main.py list-users
```

---

### Projects

**Add a project to a user:**
```bash
python main.py add-project --user "Alex" --title "CLI Tool" --description "My first CLI app"
```

**Add a project with a due date** 
```bash
python main.py add-project --user "Alex" --title "Website" --due-date "2025-12-31"
python main.py add-project --user "Alex" --title "Website" --due-date "Dec 31 2025"
python main.py add-project --user "Alex" --title "Website" --due-date "31/12/2025"
```

**List all projects:**
```bash
python main.py list-projects
```

**List projects for a specific user:**
```bash
python main.py list-projects --user "Alex"
```

**Search projects by keyword:**
```bash
python main.py search-projects --keyword "CLI"
```

---

###  Tasks

**Add a task to a project:**
```bash
python main.py add-task --project "CLI Tool" --title "Write README"
```

**Add a task with an assignee:**
```bash
python main.py add-task --project "CLI Tool" --title "Fix bugs" --assigned-to "Alex"
```

**List all tasks in a project:**
```bash
python main.py list-tasks --project "CLI Tool"
```

**Mark a task as complete** 
```bash
python main.py complete-task --id 1
```

---

## Running Tests

```bash
python3 -m unittest discover -s tests -v
```

```bash
pytest tests/ -v
```

There are two test files:
- `test_models.py` — tests the User, Project, and Task classes directly
- `test_cli.py` — tests the CLI handler functions using mock data (no files written)

---

## Features Overview

| Feature | Details |
|---|---|
| User management | Create users with name and email |
| Project management | Assign projects to users with descriptions and due dates |
| Task management | Add tasks to projects, assign them to people |
| Complete tasks | Mark individual tasks as done by ID |
| Search | Find projects across all users by keyword |
| Flexible dates | Accepts many date formats thanks to `python-dateutil` |
| Formatted tables | Clean output using `tabulate` |
| Persistence | All data auto-saved to `data/data.json` between sessions |
| Error handling | Graceful messages for missing users, bad dates, duplicates |

---

## External Packages Used

| Package | Purpose |
|---|---|
| `tabulate` | Formats data into clean, readable tables in the terminal |
| `python-dateutil` | Parses and validates date input in many different formats |
| `rich` | Coloured terminal output for success/error messages |
| `pytest` | Test runner for the unit tests (dev only) |

---

## Known Issues

- No delete command yet — to remove a user, project, or task you need to edit `data/data.json` manually
- Project titles must be unique across all users 
- No user login or authentication — all users are managed by a single admin
