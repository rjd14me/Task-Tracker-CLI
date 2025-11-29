# FlowTask (v1.1)
My personal solution to the [Task Tracker](https://roadmap.sh/projects/task-tracker) problem on [Roadmap.sh](https://roadmap.sh/dashboard).

# How to Demo
### Setting Up
```bash
git clone https://github.com/rjd14me/FlowTask.git
cd FlowTask
```
### Getting Started
```bash
python mainCLI.py 
```
```bash
command> help #to see all commands in the menu
```
## Features
- Add, update, delete tasks (with optional complete-by dates and priorities)
- Mark tasks as in-progress or done
- List tasks with optional status filtering (todo, in-progress, done)
- JSON storage in `data/tasks.json`

## Key skills demonstrated
- Command-line UX: argparse subcommands plus an interactive REPL prompt.
- Data modeling: lightweight dataclass for tasks with defaults and serialization.
- Persistence: JSON file storage with safe creation/reset handling.
- Validation: flexible date parsing/formatting and priority normalization.
- User feedback: colored output, friendly prompts, and error messaging.

## commands
```
add <task> - add you new task to the list
update <task id> <new description> - adds a new description to a task already in the list
delete <task id> - deletes a task from the list
start <task id> - marks a task as in progress.
done <task id> - marks a task as been completed.
list - lists the current task list
list-done - lists all the tasks that have been completed
list-not-done - lists all of the tasks that have not been completed.
list-in-progress - lists all the tasks currently been done.
help - displays this list of commands
```

## Project layout
```text
TASK-TRACKER/
  task_cli.py
  data/
    tasks.json  # created automatically while running program
  taskmanager/
    __init__.py
    storage.py
    models.py
    manage.py
  README.md
  LICENSE
```
