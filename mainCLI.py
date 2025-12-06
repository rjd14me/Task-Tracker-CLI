import argparse
import sys
from datetime import datetime

from taskmanager.manage import add_task, update_task, delete_task, mark_done, mark_in_progress, list_tasks

# Edit these maps to add/remove shorthand forms users can type for each command.
COMMAND_ALIASES = {
    "help": ["help", "h", "?"],
    "add": ["add", "a"],
    "update": ["update", "u"],
    "delete": ["delete", "del", "rm"],
    "start": ["start", "s"],
    "done": ["done", "d"],
    "list": ["list", "ls", "l"],
    "exit": ["exit", "quit", "q"],
    "list-done": ["list-done", "list done", "list-d", "list d", "l-d", "l d", "ld"],
    "list-not-done": ["list-not-done", "list not done", "list-nd", "list nd", "l-nd", "l nd", "lnd"],
    "list-in-progress": [
        "list-in-progress",
        "list in progress",
        "list-ip",
        "list ip",
        "l-ip",
        "l ip",
        "lip",
    ],
}

HELP_TEXT = [
    ("help", "show this list of commands"),
    ("add", "add your new task to the list"),
    ("update", "update the description of a task already in the list"),
    ("delete", "delete a task from the list"),
    ("start", "mark a task as in progress"),
    ("done", "mark a task as completed"),
    ("list", "list the current task list"),
    ("list-done", "list tasks that have been completed"),
    ("list-not-done", "list tasks that are not yet completed"),
    ("list-in-progress", "list tasks currently in progress"),
    ("exit", "exit the program"),
]


def _build_alias_lookup():
    lookup = []
    for canonical, variants in COMMAND_ALIASES.items():
        for variant in variants:
            lookup.append((variant.lower().split(), canonical))
    lookup.sort(key=lambda entry: len(entry[0]), reverse=True)
    return lookup


ALIAS_LOOKUP = _build_alias_lookup()


def display_task_list():
    tasks = list_tasks()
    print("Current tasks:")
    if not tasks:
        print("  (no tasks)")
        return
    for task in tasks:
        print(f"  {format_task(task)}")


def format_task(task):
    creation_date_raw = task.get("creation_date")
    creation_date = "Unknown"
    if creation_date_raw:
        try:
            creation_date = datetime.fromisoformat(creation_date_raw).strftime("%d/%m/%Y")
        except ValueError:
            creation_date = creation_date_raw
    due_date = task.get("due_date", "No Due Date")
    status = task.get("status", "To Do")
    return f"{task['id']}: {status} - {task['description']} (Created: {creation_date}, Due: {due_date})"


def aliases_for(command):
    """Return aliases suitable for argparse (single tokens only)."""
    return [
        alias
        for alias in COMMAND_ALIASES.get(command, [])
        if alias != command and " " not in alias
    ]


def normalize_command_tokens(tokens):
    """Normalize raw tokens to a canonical command and return leftover args."""
    if not tokens:
        return None, []
    lowered = [token.lower() for token in tokens]
    for alias_tokens, canonical in ALIAS_LOOKUP:
        if lowered[: len(alias_tokens)] == alias_tokens:
            return canonical, tokens[len(alias_tokens) :]
    return None, tokens[1:]


def normalize_cli_args(argv):
    """Rewrite argv so argparse sees the canonical command names."""
    if argv is None:
        return None
    command, remaining = normalize_command_tokens(argv)
    if command in (None, "exit"):
        return argv
    return [command] + remaining


def prompt_due_date():
    while True:
        raw = input("Enter Due Date (DD/MM/YYYY) or press Enter for 'No Due Date': ").strip()
        if not raw:
            return "No Due Date"
        try:
            # Validate and normalize format.
            parsed = datetime.strptime(raw, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format. Please use DD/MM/YYYY.")
            continue
        if parsed.date() <= datetime.now().date():
            print("Only future dates are allowed.")
            continue
        return parsed.strftime("%d/%m/%Y")


def cmd_add(args):
    description = " ".join(args.description)
    due_date = prompt_due_date()
    add_task(description, due_date)
    print("Task added.")
    display_task_list()
    return 0


def cmd_update(args):
    description = " ".join(args.description)
    update_task(args.task_id, description)
    print("Task updated.")
    display_task_list()
    return 0


def cmd_delete(args):
    delete_task(args.task_id)
    print("Task deleted.")
    display_task_list()
    return 0


def cmd_done(args):
    mark_done(args.task_id)
    print("Task marked as done.")
    display_task_list()
    return 0


def cmd_start(args):
    mark_in_progress(args.task_id)
    print("Task marked as in progress.")
    display_task_list()
    return 0


def cmd_list(args):
    tasks = list_tasks()
    for task in tasks:
        print(format_task(task))
    return 0


def cmd_list_done(args):
    tasks = list_tasks("done")
    for task in tasks:
        print(format_task(task))
    return 0


def cmd_list_not_done(args):
    tasks = list_tasks()
    for task in tasks:
        if task.get("status") != "done":
            print(format_task(task))
    return 0


def cmd_list_in_progress(args):
    tasks = list_tasks("in-progress")
    for task in tasks:
        print(format_task(task))
    return 0


def print_help_text():
    print("Available commands (aliases in brackets):")
    for command, description in HELP_TEXT:
        alias_text = ", ".join(
            alias for alias in COMMAND_ALIASES.get(command, []) if alias != command
        )
        suffix = f" [{alias_text}]" if alias_text else ""
        print(f"{command}{suffix} - {description}")


def cmd_help(args):
    print_help_text()
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Task Tracker")
    subparsers = parser.add_subparsers(dest="command")

    help_parser = subparsers.add_parser(
        "help", help="Show available commands", aliases=aliases_for("help")
    )
    help_parser.set_defaults(func=cmd_help)

    add_parser = subparsers.add_parser(
        "add", help="Add a new task", aliases=aliases_for("add")
    )
    add_parser.add_argument("description", nargs="+", help="Task description")
    add_parser.set_defaults(func=cmd_add)

    update_parser = subparsers.add_parser(
        "update", help="Update a task description", aliases=aliases_for("update")
    )
    update_parser.add_argument("task_id", type=int, help="ID of the task to update")
    update_parser.add_argument("description", nargs="+", help="New description")
    update_parser.set_defaults(func=cmd_update)

    delete_parser = subparsers.add_parser(
        "delete", help="Delete a task", aliases=aliases_for("delete")
    )
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")
    delete_parser.set_defaults(func=cmd_delete)

    start_parser = subparsers.add_parser(
        "start", help="Mark a task as in progress", aliases=aliases_for("start")
    )
    start_parser.add_argument("task_id", type=int, help="ID of the task to update")
    start_parser.set_defaults(func=cmd_start)

    done_parser = subparsers.add_parser(
        "done", help="Mark a task as done", aliases=aliases_for("done")
    )
    done_parser.add_argument("task_id", type=int, help="ID of the task to update")
    done_parser.set_defaults(func=cmd_done)

    list_parser = subparsers.add_parser(
        "list", help="List all tasks", aliases=aliases_for("list")
    )
    list_parser.set_defaults(func=cmd_list)

    list_done_parser = subparsers.add_parser(
        "list-done", help="List done tasks", aliases=aliases_for("list-done")
    )
    list_done_parser.set_defaults(func=cmd_list_done)

    list_not_done_parser = subparsers.add_parser(
        "list-not-done",
        help="List tasks that are not done",
        aliases=aliases_for("list-not-done"),
    )
    list_not_done_parser.set_defaults(func=cmd_list_not_done)

    list_in_progress_parser = subparsers.add_parser(
        "list-in-progress",
        help="List tasks in progress",
        aliases=aliases_for("list-in-progress"),
    )
    list_in_progress_parser.set_defaults(func=cmd_list_in_progress)

    return parser


def run_prompt():
    print("Task Tracker. Type exit to quit.")
    while True:
        raw = input("command> ").strip()
        if not raw:
            continue
        command, args = normalize_command_tokens(raw.split())
        if command == "exit":
            break
        if command is None:
            print("Unknown command.")
            continue
        if command == "help":
            print_help_text()
        elif command == "add":
            if not args:
                print("Need a description.")
                continue
            description = " ".join(args)
            due_date = prompt_due_date()
            add_task(description, due_date)
            print("Task added.")
            display_task_list()
        elif command == "update":
            if len(args) < 2:
                print("Need id and description.")
                continue
            try:
                task_id = int(args[0])
            except ValueError:
                print("Task id must be a number.")
                continue
            update_task(task_id, " ".join(args[1:]))
            print("Task updated.")
            display_task_list()
        elif command == "delete":
            if not args:
                print("Need an id.")
                continue
            try:
                task_id = int(args[0])
            except ValueError:
                print("Task id must be a number.")
                continue
            delete_task(task_id)
            print("Task deleted.")
            display_task_list()
        elif command == "start":
            if not args:
                print("Need an id.")
                continue
            try:
                task_id = int(args[0])
            except ValueError:
                print("Task id must be a number.")
                continue
            mark_in_progress(task_id)
            print("Task marked as in progress.")
            display_task_list()
        elif command == "done":
            if not args:
                print("Need an id.")
                continue
            try:
                task_id = int(args[0])
            except ValueError:
                print("Task id must be a number.")
                continue
            mark_done(task_id)
            print("Task marked as done.")
            display_task_list()
        elif command == "list":
            for task in list_tasks():
                print(format_task(task))
        elif command == "list-done":
            for task in list_tasks("done"):
                print(format_task(task))
        elif command == "list-not-done":
            for task in list_tasks():
                if task.get("status") != "done":
                    print(format_task(task))
        elif command == "list-in-progress":
            for task in list_tasks("in-progress"):
                print(format_task(task))
        else:
            print("Unknown command.")


def main(argv=None):
    parser = build_parser()
    raw_args = argv if argv is not None else sys.argv[1:]
    normalized_args = normalize_cli_args(raw_args)
    args = parser.parse_args(normalized_args)

    if not getattr(args, "command", None):
        return run_prompt()

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
