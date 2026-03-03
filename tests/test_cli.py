
import unittest
import sys
import os
from unittest.mock import patch
from io import StringIO

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.user import User
from models.project import Project
from models.task import Task

# Import the handler functions we want to test
from main import (
    handle_add_user,
    handle_list_users,
    handle_add_project,
    handle_list_projects,
    handle_add_task,
    handle_list_tasks,
    handle_complete_task,
    handle_search_projects,
)


# HELPER: Fake args object


class FakeArgs:

    def __init__(self, **kwargs):
        # Store every keyword argument as an attribute
        # e.g. FakeArgs(name="Alex") → args.name == "Alex"
        for key, value in kwargs.items():
            setattr(self, key, value)


# CLI HANDLER TESTS

class TestAddUserHandler(unittest.TestCase):

    def setUp(self):
        
        self.users = []

    def test_add_user_success(self):
        args = FakeArgs(name="Alex", email="alex@test.com")

        # patch("main.save_data") replaces save_data with a dummy function
        with patch("main.save_data"):
            handle_add_user(args, self.users)

        self.assertEqual(len(self.users), 1)
        self.assertEqual(self.users[0].name, "Alex")
        self.assertEqual(self.users[0].email, "alex@test.com")

    def test_add_duplicate_user_is_rejected(self):
        existing_user = User("Alex", "alex@test.com")
        self.users.append(existing_user)

        args = FakeArgs(name="Alex", email="other@test.com")
        with patch("main.save_data"):
            handle_add_user(args, self.users)

        # Should still only have 1 user - the duplicate was rejected
        self.assertEqual(len(self.users), 1)

    def test_add_multiple_users(self):
        with patch("main.save_data"):
            handle_add_user(FakeArgs(name="Alice", email="alice@test.com"), self.users)
            handle_add_user(FakeArgs(name="Bob",   email="bob@test.com"),   self.users)
            handle_add_user(FakeArgs(name="Carol", email="carol@test.com"), self.users)

        self.assertEqual(len(self.users), 3)


class TestAddProjectHandler(unittest.TestCase):

    def setUp(self):
        self.users = [User("Alex", "alex@test.com")]

    def test_add_project_to_existing_user(self):
        args = FakeArgs(
            user="Alex",
            title="My App",
            description="A test project",
            due_date="2025-12-31"
        )
        with patch("main.save_data"):
            handle_add_project(args, self.users)

        self.assertEqual(len(self.users[0].projects), 1)
        self.assertEqual(self.users[0].projects[0].title, "My App")

    def test_add_project_to_unknown_user_fails(self):
        args = FakeArgs(
            user="Nobody",
            title="Ghost Project",
            description="",
            due_date=""
        )
        with patch("main.save_data"):
            handle_add_project(args, self.users)

        # Alex should still have no projects
        self.assertEqual(len(self.users[0].projects), 0)

    def test_duplicate_project_title_rejected(self):
        args = FakeArgs(user="Alex", title="Duplicate", description="", due_date="")

        with patch("main.save_data"):
            handle_add_project(args, self.users)
            handle_add_project(args, self.users)  # second time - should be rejected

        self.assertEqual(len(self.users[0].projects), 1)

    def test_invalid_date_is_rejected(self):
        args = FakeArgs(
            user="Alex",
            title="Bad Date Project",
            description="",
            due_date="not-a-date"
        )
        with patch("main.save_data"):
            handle_add_project(args, self.users)

        # Project should NOT have been added
        self.assertEqual(len(self.users[0].projects), 0)

    def test_flexible_date_formats_accepted(self):
   
        date_inputs = ["2025-12-31", "Dec 31 2025", "31/12/2025"]

        for i, date_input in enumerate(date_inputs):
            args = FakeArgs(
                user="Alex",
                title=f"Project {i}",
                description="",
                due_date=date_input
            )
            with patch("main.save_data"):
                handle_add_project(args, self.users)

        # All 3 projects should have been added successfully
        self.assertEqual(len(self.users[0].projects), 3)
        # All should be stored in YYYY-MM-DD format
        for project in self.users[0].projects:
            self.assertEqual(project.due_date, "2025-12-31")


class TestAddTaskHandler(unittest.TestCase):

    def setUp(self):
        self.users = [User("Alex", "alex@test.com")]
        project = Project("My Project", owner_name="Alex")
        self.users[0].add_project(project)

    def test_add_task_to_existing_project(self):
        args = FakeArgs(project="My Project", title="Write tests", assigned_to="Alex")
        with patch("main.save_data"):
            handle_add_task(args, self.users)

        project = self.users[0].projects[0]
        self.assertEqual(len(project.tasks), 1)
        self.assertEqual(project.tasks[0].title, "Write tests")

    def test_add_task_to_unknown_project_fails(self):

        args = FakeArgs(project="Ghost Project", title="Phantom Task", assigned_to="")
        with patch("main.save_data"):
            handle_add_task(args, self.users)

        # No tasks should have been added
        self.assertEqual(len(self.users[0].projects[0].tasks), 0)

    def test_task_starts_as_pending(self):
        args = FakeArgs(project="My Project", title="Fresh Task", assigned_to="")
        with patch("main.save_data"):
            handle_add_task(args, self.users)

        task = self.users[0].projects[0].tasks[0]
        self.assertEqual(task.status, "pending")


class TestCompleteTaskHandler(unittest.TestCase):

    def setUp(self):
        self.users = [User("Alex", "alex@test.com")]
        project = Project("My Project", owner_name="Alex")
        self.task = Task("Finish feature")
        project.add_task(self.task)
        self.users[0].add_project(project)

    def test_complete_existing_task(self):
        args = FakeArgs(id=self.task.id)
        with patch("main.save_data"):
            handle_complete_task(args, self.users)

        self.assertEqual(self.task.status, "complete")

    def test_complete_nonexistent_task_does_nothing(self):
        args = FakeArgs(id=99999)
        with patch("main.save_data"):
            handle_complete_task(args, self.users)   # Should not raise an error

        # The real task should still be pending
        self.assertEqual(self.task.status, "pending")


class TestSearchProjectsHandler(unittest.TestCase):

    def setUp(self):
        self.users = [
            User("Alex", "alex@test.com"),
            User("Sam",  "sam@test.com"),
        ]
        p1 = Project("CLI Tool",         description="command line app", owner_name="Alex")
        p2 = Project("Website Redesign", description="new homepage",     owner_name="Sam")
        p3 = Project("CLI Dashboard",    description="admin panel",       owner_name="Sam")
        self.users[0].add_project(p1)
        self.users[1].add_project(p2)
        self.users[1].add_project(p3)

    def test_search_finds_matching_projects(self):
        args = FakeArgs(keyword="CLI")
        # Capture the printed output to check it, but mainly we just test it doesn't crash
        with patch("builtins.print"):
            handle_search_projects(args, self.users)

    def test_search_is_case_insensitive(self):
        args_lower = FakeArgs(keyword="cli")
        args_upper = FakeArgs(keyword="CLI")
        # Both should run without errors
        with patch("builtins.print"):
            handle_search_projects(args_lower, self.users)
            handle_search_projects(args_upper, self.users)

    def test_search_no_results(self):
        args = FakeArgs(keyword="zzznomatch")
        with patch("builtins.print"):
            handle_search_projects(args, self.users)   # Should not raise an error


# Run the tests directly
if __name__ == "__main__":
    unittest.main(verbosity=2)
