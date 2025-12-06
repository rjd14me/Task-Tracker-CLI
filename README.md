# FlowTask (v1.6)
My personal solution to the [Task Tracker](https://roadmap.sh/projects/task-tracker) problem on [Roadmap.sh](https://roadmap.sh/dashboard).

# How to Demo
### Setting Up
```
Requires Python 3.12.x +
```
```bash
git clone https://github.com/rjd14me/FlowTask.git
cd FlowTask
```
### Getting Started
```bash
python mainCLI.py 
```
```bash
command> help #to see all commands
```
## Features
- Add, update, delete tasks (with optional complete-by dates and priorities)
- Mark tasks as in-progress or done
- List tasks with optional status filtering (todo, in-progress, done)
- JSON storage in `data/tasks.json`
- Track the date the tasks were added (DD/MM/YYYY).
- Allow users to input a due by date, no defaulting to no due date if no input
- Allows user to format commands in multiple ways for ease of use
- Interactive REPL starts when no CLI subcommand is given, mirroring the argparse commands.
- Due-date prompt enforces DD/MM/YYYY and only accepts future dates; users can opt out with Enter.
- Data store auto-creates data/tasks.json and self-heals if the JSON is invalid.
- Deleting a task re-sequences IDs to keep the list tidy.

## Key skills demonstrated
- Command-line UX: argparse subcommands plus an interactive REPL prompt.
- Data modeling: lightweight dataclass for tasks with defaults and serialization.
- Persistence: JSON file storage with safe creation/reset handling.
- Validation: flexible date parsing/formatting and priority normalization.
- User feedback: colored output, friendly prompts, and error messaging.
- Command alias normalization across argparse and an interactive REPL.
- Robust input validation (date format + future-only constraint) with user-friendly feedback.
- Resilient persistence layer with auto-creation and corruption recovery for JSON storage.

## Commands
```
help [h|?]                    show available commands and aliases
add <description> [a]         add a new task (prompts for a future due date or “No Due Date”)
update <id> <description> [u] update an existing task description
delete <id> [del|rm]          delete a task and reindex IDs
start <id> [s]                mark a task as in progress
done <id> [d]                 mark a task as completed
list [ls|l]                   list all tasks
list-done [list d|ld]         list tasks marked completed
list-not-done [list nd|lnd]   list tasks not yet completed
list-in-progress [list ip|lip] list tasks currently in progress
exit [quit|q]                 exit the interactive prompt
```

## Project layout
```text
TASK-TRACKER/
  task_cli.py
  data/
    tasks.json 
  taskmanager/
    __init__.py
    storage.py
    models.py
    manage.py
  README.md
  LICENSE
```
