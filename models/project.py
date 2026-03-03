# This file defines the Project class
# Each project belongs to one user and can have many tasks


class Project:

    # Class attribute: auto-increments to give each project a unique ID
    _id_counter = 1

    def __init__(self, title, description="", due_date="", owner_name=""):
        self.id = Project._id_counter
        Project._id_counter += 1

        self._title = title
        self._description = description
        self._due_date = due_date        # Expected format: YYYY-MM-DD
        self.owner_name = owner_name     # The name of the user who owns this project

        # A list to store all tasks in this project
        self.tasks = []

    # Properties (getters and setters) 

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Title must be a non-empty string")
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, value):
        self._due_date = value

    # Methods 

    def add_task(self, task):
        self.tasks.append(task)

    def get_tasks(self):
        return self.tasks

    def get_completed_tasks(self):
        return [task for task in self.tasks if task.status == "complete"]

    def get_pending_tasks(self):
        return [task for task in self.tasks if task.status == "pending"]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "owner_name": self.owner_name,
            "tasks": [t.to_dict() for t in self.tasks]
        }

    @classmethod
    def from_dict(cls, data):
        from models.task import Task

        project = cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            owner_name=data.get("owner_name", "")
        )
        project.id = data["id"]

        # Rebuild each task from saved data
        for task_data in data.get("tasks", []):
            task = Task.from_dict(task_data)
            project.tasks.append(task)

        return project

    def __str__(self):
        task_count = len(self.tasks)
        done = len(self.get_completed_tasks())
        due = f" | Due: {self._due_date}" if self._due_date else ""
        return (
            f"[ID: {self.id}] {self._title}{due} | "
            f"Tasks: {done}/{task_count} complete"
        )

    def __repr__(self):
        return f"Project(title={self._title})"
