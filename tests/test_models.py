# Unit tests for our User, Project, and Task classes

import unittest  
import sys
import os

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

# Add the project root to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.user import User
from models.project import Project
from models.task import Task


# USER TESTS

class TestUser(unittest.TestCase):

    def test_create_user(self):
        user = User("Alice", "alice@test.com")
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.email, "alice@test.com")

    def test_user_has_unique_id(self):
        user1 = User("Bob", "bob@test.com")
        user2 = User("Carol", "carol@test.com")
        self.assertNotEqual(user1.id, user2.id)

    def test_user_starts_with_no_projects(self):
        user = User("Dave", "dave@test.com")
        self.assertEqual(user.projects, [])
        self.assertEqual(len(user.projects), 0)

    def test_add_project_to_user(self):
        user = User("Eve", "eve@test.com")
        project = Project("Test Project")
        user.add_project(project)
        self.assertEqual(len(user.projects), 1)
        self.assertEqual(user.projects[0].title, "Test Project")

    def test_user_to_dict(self):
        user = User("Frank", "frank@test.com")
        data = user.to_dict()
        self.assertEqual(data["name"], "Frank")
        self.assertEqual(data["email"], "frank@test.com")
        self.assertIn("projects", data)

    def test_user_from_dict(self):
        data = {
            "id": 99,
            "name": "Grace",
            "email": "grace@test.com",
            "projects": []
        }
        user = User.from_dict(data)
        self.assertEqual(user.name, "Grace")
        self.assertEqual(user.email, "grace@test.com")

    def test_invalid_email_raises_error(self):
        user = User("Test", "test@test.com")
        with self.assertRaises(ValueError):
            user.email = "not-a-valid-email"

    def test_invalid_name_raises_error(self):
        user = User("Test", "test@test.com")
        with self.assertRaises(ValueError):
            user.name = ""


# PROJECT TESTS

class TestProject(unittest.TestCase):

    def test_create_project(self):
        project = Project("Build App", description="A mobile app", due_date="2025-12-01")
        self.assertEqual(project.title, "Build App")
        self.assertEqual(project.description, "A mobile app")
        self.assertEqual(project.due_date, "2025-12-01")

    def test_project_starts_with_no_tasks(self):
        project = Project("Empty Project")
        self.assertEqual(project.tasks, [])

    def test_add_task_to_project(self):
        project = Project("My Project")
        task = Task("Write tests")
        project.add_task(task)
        self.assertEqual(len(project.tasks), 1)

    def test_get_pending_tasks(self):
        project = Project("My Project")
        task1 = Task("Task 1")
        task2 = Task("Task 2", status="complete")
        project.add_task(task1)
        project.add_task(task2)
        pending = project.get_pending_tasks()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].title, "Task 1")

    def test_get_completed_tasks(self):
        project = Project("My Project")
        task1 = Task("Task A")
        task2 = Task("Task B")
        task2.mark_complete()
        project.add_task(task1)
        project.add_task(task2)
        completed = project.get_completed_tasks()
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0].title, "Task B")

    def test_project_to_dict(self):
        project = Project("Dict Test", description="Testing to_dict")
        data = project.to_dict()
        self.assertEqual(data["title"], "Dict Test")
        self.assertEqual(data["description"], "Testing to_dict")
        self.assertIn("tasks", data)



# TASK TESTS

class TestTask(unittest.TestCase):

    def test_create_task(self):
        task = Task("Write documentation", assigned_to="Alice")
        self.assertEqual(task.title, "Write documentation")
        self.assertEqual(task.assigned_to, "Alice")
        self.assertEqual(task.status, "pending")

    def test_mark_complete(self):
        task = Task("Do something")
        self.assertEqual(task.status, "pending")
        task.mark_complete()
        self.assertEqual(task.status, "complete")

    def test_invalid_status_raises_error(self):
        task = Task("Test Task")
        with self.assertRaises(ValueError):
            task.status = "in-progress"

    def test_task_to_dict(self):
        task = Task("Code review", assigned_to="Bob")
        data = task.to_dict()
        self.assertEqual(data["title"], "Code review")
        self.assertEqual(data["assigned_to"], "Bob")
        self.assertEqual(data["status"], "pending")

    def test_task_from_dict(self):
        data = {
            "id": 10,
            "title": "Deploy app",
            "assigned_to": "Carol",
            "status": "complete"
        }
        task = Task.from_dict(data)
        self.assertEqual(task.title, "Deploy app")
        self.assertEqual(task.status, "complete")


class TestIntegration(unittest.TestCase):

    def test_full_workflow(self):
        
        user = User("Integration User", "integration@test.com")
        self.assertEqual(len(user.projects), 0)

        project = Project("Integration Project", owner_name=user.name)
        user.add_project(project)
        self.assertEqual(len(user.projects), 1)

        task1 = Task("First Task")
        task2 = Task("Second Task")
        project.add_task(task1)
        project.add_task(task2)
        self.assertEqual(len(project.tasks), 2)

        task1.mark_complete()
        self.assertEqual(len(project.get_completed_tasks()), 1)
        self.assertEqual(len(project.get_pending_tasks()), 1)

    def test_serialization_round_trip(self):
        user = User("Serial User", "serial@test.com")
        project = Project("Serial Project", description="Test persistence")
        task = Task("Serial Task", assigned_to="Tester")
        task.mark_complete()

        project.add_task(task)
        user.add_project(project)

        user_dict = user.to_dict()
        restored_user = User.from_dict(user_dict)

        self.assertEqual(restored_user.name, "Serial User")
        self.assertEqual(len(restored_user.projects), 1)
        self.assertEqual(restored_user.projects[0].title, "Serial Project")
        self.assertEqual(len(restored_user.projects[0].tasks), 1)
        self.assertEqual(restored_user.projects[0].tasks[0].status, "complete")


if __name__ == "__main__":
    unittest.main(verbosity=2)
