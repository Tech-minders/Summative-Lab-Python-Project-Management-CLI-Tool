# This file defines the Task class
# Each task belongs to one project


class Task:
    # Class attribute for unique IDs
    _id_counter = 1

    def __init__(self, title, assigned_to="", status="pending"):
        self.id = Task._id_counter
        Task._id_counter += 1

        self._title = title
        self._assigned_to = assigned_to   # Name of the person doing this task
        self._status = status             # Either "pending" or "complete"

    # Properties 

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Task title must be a non-empty string")
        self._title = value

    @property
    def assigned_to(self):
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value):
        self._assigned_to = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        # Only allow valid status values
        if value not in ("pending", "complete"):
            raise ValueError("Status must be 'pending' or 'complete'")
        self._status = value

    # Methods 

    def mark_complete(self):
        self._status = "complete"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self._title,
            "assigned_to": self._assigned_to,
            "status": self._status
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data["title"],
            assigned_to=data.get("assigned_to", ""),
            status=data.get("status", "pending")
        )
        task.id = data["id"]
        return task

    def __str__(self):
        
        assigned = f" | Assigned to: {self._assigned_to}" if self._assigned_to else ""
        return f" [ID: {self.id}] {self._title}{assigned} [{self._status}]"

    def __repr__(self):
        return f"Task(title={self._title}, status={self._status})"
