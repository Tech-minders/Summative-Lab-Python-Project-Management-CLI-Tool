# This file contains helper functions used throughout the app.

from tabulate import tabulate

from dateutil import parser as date_parser

# Try to import 'rich' for coloured console output.
# Falls back gracefully if rich is not installed.
try:
    from rich.console import Console
    from rich.table import Table
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    import re
    class Console:
        def print(self, text, *args, **kwargs):
            # Strip any [color] tags that rich uses, e.g. [green], [/green]
            clean = re.sub(r'\[/?[^\]]+\]', '', str(text))
            print(clean)
    console = Console()



def validate_date(date_str):
    
    if not date_str:
        return ""
    try:
        # parse() figures out the date format automatically
        parsed = date_parser.parse(date_str)
        # Return in a standard format so all dates look the same in our data
        return parsed.strftime("%Y-%m-%d")
    except (ValueError, OverflowError):
        # dateutil couldn't understand the date string
        return None


# SEARCH HELPERS

def find_user_by_name(users, name):

    name_lower = name.lower()
    for user in users:
        if user.name.lower() == name_lower:
            return user
    return None


def find_project_by_title(users, title):

    title_lower = title.lower()
    for user in users:
        for project in user.projects:
            if project.title.lower() == title_lower:
                return project
    return None


def find_task_by_id(users, task_id):

    for user in users:
        for project in user.projects:
            for task in project.tasks:
                if task.id == task_id:
                    return task
    return None


# TABLE DISPLAY HELPERS (uses tabulate)

def print_users_table(users):
 
    if not users:
        console.print("[yellow]No users found.[/yellow]")
        return

    # Build rows as a list of lists - tabulate expects this format
    rows = [[u.id, u.name, u.email, len(u.projects)] for u in users]
    headers = ["ID", "Name", "Email", "Projects"]

    # tabulate() returns a nicely formatted string
    # "rounded_outline" is one of many available styles
    table_str = tabulate(rows, headers=headers, tablefmt="rounded_outline")

    print("\n  👥 All Users")
    print(table_str)


def print_projects_table(projects, owner_name=""):

    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    rows = []
    for p in projects:
        done = len(p.get_completed_tasks())
        total = len(p.tasks)
        rows.append([p.id, p.title, p.description or "-", p.due_date or "-", f"{done}/{total}"])

    headers = ["ID", "Title", "Description", "Due Date", "Tasks Done"]
    table_str = tabulate(rows, headers=headers, tablefmt="rounded_outline")

    title = f"📁 Projects for {owner_name}" if owner_name else "📁 All Projects"
    print(f"\n  {title}")
    print(table_str)


def print_tasks_table(tasks, project_title=""):

    if not tasks:
        console.print("[yellow]No tasks found.[/yellow]")
        return

    rows = []
    for task in tasks:
        rows.append([task.id, task.title, task.assigned_to or "-", f" {task.status}"])

    headers = ["ID", "Title", "Assigned To", "Status"]
    table_str = tabulate(rows, headers=headers, tablefmt="rounded_outline")

    title = f" Tasks in '{project_title}'" if project_title else " Tasks"
    print(f"\n  {title}")
    print(table_str)
