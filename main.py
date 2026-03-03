# This is the entry point for our CLI application.


import argparse  

from models.user import User
from models.project import Project
from models.task import Task
from utils.file_io import save_data, load_data
from utils.helpers import (
    find_user_by_name,
    find_project_by_title,
    find_task_by_id,
    print_users_table,
    print_projects_table,
    print_tasks_table
)
try:
    from rich.console import Console
    console = Console()
except ImportError:
    import re
    class Console:
        def print(self, text, *args, **kwargs):
            clean = re.sub(r'\[/?[^\]]+\]', '', str(text))
            print(clean)
    console = Console()


# COMMAND HANDLER FUNCTIONS

def handle_add_user(args, users):
    # Check if a user with this name already exists
    existing = find_user_by_name(users, args.name)
    if existing:
        console.print(f"[red] A user named '{args.name}' already exists.[/red]")
        return

    # Create a new User object
    try:
        new_user = User(name=args.name, email=args.email)
    except ValueError as e:
        console.print(f"[red] Error: {e}[/red]")
        return

    # Add to our list and save
    users.append(new_user)
    save_data(users)
    console.print(f"[green] User '{args.name}' added successfully![/green]")


def handle_list_users(args, users):
    print_users_table(users)


def handle_add_project(args, users):
    # Find the user who will own this project
    user = find_user_by_name(users, args.user)
    if not user:
        console.print(f"[red] No user found with name '{args.user}'.[/red]")
        return

    # Check if project title already exists for this user
    for p in user.projects:
        if p.title.lower() == args.title.lower():
            console.print(f"[red] '{args.user}' already has a project called '{args.title}'.[/red]")
            return

    # Create and assign the project
    try:
        project = Project(
            title=args.title,
            description=args.description or "",
            due_date=args.due_date or "",
            owner_name=user.name
        )
    except ValueError as e:
        console.print(f"[red] Error: {e}[/red]")
        return

    user.add_project(project)
    save_data(users)
    console.print(f"[green] Project '{args.title}' added to {args.user}![/green]")


def handle_list_projects(args, users):
    if args.user:
        # Show projects for a specific user
        user = find_user_by_name(users, args.user)
        if not user:
            console.print(f"[red] No user found with name '{args.user}'.[/red]")
            return
        print_projects_table(user.projects, owner_name=user.name)
    else:
        # Show all projects from all users
        all_projects = []
        for user in users:
            all_projects.extend(user.projects)
        print_projects_table(all_projects)


def handle_add_task(args, users):
    # Find the project to add the task to
    project = find_project_by_title(users, args.project)
    if not project:
        console.print(f"[red] No project found with title '{args.project}'.[/red]")
        return

    # Create and add the task
    try:
        task = Task(
            title=args.title,
            assigned_to=args.assigned_to or ""
        )
    except ValueError as e:
        console.print(f"[red] Error: {e}[/red]")
        return

    project.add_task(task)
    save_data(users)
    console.print(f"[green] Task '{args.title}' added to project '{args.project}'![/green]")


def handle_list_tasks(args, users):
    project = find_project_by_title(users, args.project)
    if not project:
        console.print(f"[red] No project found with title '{args.project}'.[/red]")
        return
    print_tasks_table(project.tasks, project_title=project.title)


def handle_complete_task(args, users):
    task = find_task_by_id(users, args.id)
    if not task:
        console.print(f"[red] No task found with ID {args.id}.[/red]")
        return

    if task.status == "complete":
        console.print(f"[yellow]  Task '{task.title}' is already complete.[/yellow]")
        return

    task.mark_complete()
    save_data(users)
    console.print(f"[green] Task '{task.title}' marked as complete![/green]")


def handle_search_projects(args, users):
    keyword = args.keyword.lower()
    results = []

    for user in users:
        for project in user.projects:
            # Search in both title and description
            if keyword in project.title.lower() or keyword in project.description.lower():
                results.append(project)

    if results:
        console.print(f"[cyan]🔍 Found {len(results)} project(s) matching '{args.keyword}':[/cyan]")
        print_projects_table(results)
    else:
        console.print(f"[yellow]No projects found matching '{args.keyword}'.[/yellow]")


# CLI SETUP WITH ARGPARSE

def build_parser():

    # The main parser for our program
    parser = argparse.ArgumentParser(
        prog="project-manager",
        description="A CLI tool to manage users, projects, and tasks."
    )

    # subparsers lets us define sub-commands like 'add-user', 'list-users'.
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # add-user 
    p_add_user = subparsers.add_parser("add-user", help="Add a new user")
    p_add_user.add_argument("--name",  required=True, help="User's full name")
    p_add_user.add_argument("--email", required=True, help="User's email address")

    # list-users
    subparsers.add_parser("list-users", help="List all users")

    # add-project
    p_add_proj = subparsers.add_parser("add-project", help="Add a project to a user")
    p_add_proj.add_argument("--user",        required=True, help="Name of the user who owns this project")
    p_add_proj.add_argument("--title",       required=True, help="Project title")
    p_add_proj.add_argument("--description", default="",   help="Short description of the project")
    p_add_proj.add_argument("--due-date",    default="",   help="Due date (YYYY-MM-DD format)")

    # list-projects 
    p_list_proj = subparsers.add_parser("list-projects", help="List projects (all or by user)")
    p_list_proj.add_argument("--user", default="", help="Filter by user name (optional)")

    # add-task 
    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project",     required=True, help="Title of the project")
    p_add_task.add_argument("--title",       required=True, help="Task title")
    p_add_task.add_argument("--assigned-to", default="",   help="Name of person assigned to this task")

    # list-tasks 
    p_list_tasks = subparsers.add_parser("list-tasks", help="List all tasks in a project")
    p_list_tasks.add_argument("--project", required=True, help="Title of the project")

    # complete-task 
    p_complete = subparsers.add_parser("complete-task", help="Mark a task as complete")
    p_complete.add_argument("--id", required=True, type=int, help="The ID number of the task")

    # search-projects 
    p_search = subparsers.add_parser("search-projects", help="Search projects by keyword")
    p_search.add_argument("--keyword", required=True, help="Keyword to search for")

    return parser


# MAIN ENTRY POINT

def main():
    parser = build_parser()
    args = parser.parse_args()

    # If no command was given, show help
    if not args.command:
        parser.print_help()
        return

    # Load existing data from the JSON file
    users = load_data()

    # Map each command string to its handler function
    command_map = {
        "add-user":       handle_add_user,
        "list-users":     handle_list_users,
        "add-project":    handle_add_project,
        "list-projects":  handle_list_projects,
        "add-task":       handle_add_task,
        "list-tasks":     handle_list_tasks,
        "complete-task":  handle_complete_task,
        "search-projects": handle_search_projects,
    }

    # Get the right function and call it
    handler = command_map.get(args.command)
    if handler:
        handler(args, users)
    else:
        console.print(f"[red] Unknown command: {args.command}[/red]")
        parser.print_help()


if __name__ == "__main__":
    main()
