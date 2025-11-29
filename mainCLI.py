import argparse
import sys

from taskmanager.manage import add_task, update_task, delete_task, mark_done, mark_in_progress, list_tasks


def cmd_add(args):
    description = " ".join(args.description)
    add_task(description)
    print("Task added.")
    return 0


def cmd_update(args):
    description = " ".join(args.description)
    update_task(args.task_id, description)
    print("Task updated.")
    return 0


def cmd_delete(args):
    delete_task(args.task_id)
    print("Task deleted.")
    return 0


def cmd_done(args):
    mark_done(args.task_id)
    print("Task marked as done.")
    return 0


def cmd_start(args):
    mark_in_progress(args.task_id)
    print("Task marked as in progress.")
    return 0


def cmd_list(args):
    tasks = list_tasks()
    for task in tasks:
        print(f"{task['id']}: {task['status']} - {task['description']}")
    return 0


def cmd_list_done(args):
    tasks = list_tasks("done")
    for task in tasks:
        print(f"{task['id']}: {task['status']} - {task['description']}")
    return 0


def cmd_list_not_done(args):
    tasks = list_tasks()
    for task in tasks:
        if task.get("status") != "done":
            print(f"{task['id']}: {task['status']} - {task['description']}")
    return 0


def cmd_list_in_progress(args):
    tasks = list_tasks("in-progress")
    for task in tasks:
        print(f"{task['id']}: {task['status']} - {task['description']}")
    return 0


def print_help_text():
    print("help - show this list of commands")
    print("add <task> - add your new task to the list")
    print("update <task id> <new description> - adds a new description to a task already in the list")
    print("delete <task id> - deletes a task from the list")
    print("start <task id> - marks a task as in progress.")
    print("done <task id> - marks a task as been completed.")
    print("list - lists the current task list")
    print("list-done - lists all the tasks that have been completed")
    print("list-not-done - lists all of the tasks that have not been completed.")
    print("list-in-progress - lists all the tasks currently been done.")


def cmd_help(args):
    print_help_text()
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="Task Tracker")
    subparsers = parser.add_subparsers(dest="command")

    help_parser = subparsers.add_parser("help", help="Show available commands")
    help_parser.set_defaults(func=cmd_help)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", nargs="+", help="Task description")
    add_parser.set_defaults(func=cmd_add)

    update_parser = subparsers.add_parser("update", help="Update a task description")
    update_parser.add_argument("task_id", type=int, help="ID of the task to update")
    update_parser.add_argument("description", nargs="+", help="New description")
    update_parser.set_defaults(func=cmd_update)

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="ID of the task to delete")
    delete_parser.set_defaults(func=cmd_delete)

    start_parser = subparsers.add_parser("start", help="Mark a task as in progress")
    start_parser.add_argument("task_id", type=int, help="ID of the task to update")
    start_parser.set_defaults(func=cmd_start)

    done_parser = subparsers.add_parser("done", help="Mark a task as done")
    done_parser.add_argument("task_id", type=int, help="ID of the task to update")
    done_parser.set_defaults(func=cmd_done)

    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.set_defaults(func=cmd_list)

    list_done_parser = subparsers.add_parser("list-done", help="List done tasks")
    list_done_parser.set_defaults(func=cmd_list_done)

    list_not_done_parser = subparsers.add_parser("list-not-done", help="List tasks that are not done")
    list_not_done_parser.set_defaults(func=cmd_list_not_done)

    list_in_progress_parser = subparsers.add_parser("list-in-progress", help="List tasks in progress")
    list_in_progress_parser.set_defaults(func=cmd_list_in_progress)

    return parser


def run_prompt():
    print("Task Tracker. Type exit to quit.")
    while True:
        raw = input("command> ").strip()
        if not raw:
            continue
        if raw.lower() == "exit":
            break
        parts = raw.split()
        cmd = parts[0]
        args = parts[1:]
        if cmd == "help":
            print_help_text()
        elif cmd == "add":
            if not args:
                print("Need a description.")
                continue
            add_task(" ".join(args))
            print("Task added.")
        elif cmd == "update":
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
        elif cmd == "delete":
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
        elif cmd == "start":
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
        elif cmd == "done":
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
        elif cmd == "list":
            for task in list_tasks():
                print(f"{task['id']}: {task['status']} - {task['description']}")
        elif cmd == "list-done":
            for task in list_tasks("done"):
                print(f"{task['id']}: {task['status']} - {task['description']}")
        elif cmd == "list-not-done":
            for task in list_tasks():
                if task.get("status") != "done":
                    print(f"{task['id']}: {task['status']} - {task['description']}")
        elif cmd == "list-in-progress":
            for task in list_tasks("in-progress"):
                print(f"{task['id']}: {task['status']} - {task['description']}")
        else:
            print("Unknown command.")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if not getattr(args, "command", None):
        return run_prompt()

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
