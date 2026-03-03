# This file defines the Person base class and the User class


class Person:
  

    def __init__(self, name, email):
        # __init__ is called automatically when you create a new object
        # 'self' refers to the object being created
        self._name = name      # underscore means "private" - use property to access
        self._email = email

    # @property lets us access _name like an attribute: user.name
    @property
    def name(self):
        return self._name

    # @name.setter lets us change the value: user.name = "New Name"
    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not value or "@" not in value:
            raise ValueError("Email must contain '@'")
        self._email = value

    def __str__(self):
        # __str__ controls how the object looks when printed
        return f"{self._name} ({self._email})"


class User(Person):
    # Class attribute: shared by ALL User objects, not just one
    # We use this to give each user a unique ID number
    _id_counter = 1

    def __init__(self, name, email):
        # Call the parent class (Person) __init__ first
        super().__init__(name, email)

        # Give this user a unique ID
        self.id = User._id_counter
        User._id_counter += 1

        # A list to store all projects belonging to this user
        # This creates a one-to-many relationship: one user -> many projects
        self.projects = []

    def add_project(self, project):
        self.projects.append(project)

    def get_projects(self):
        return self.projects

    def to_dict(self):
        
        return {
            "id": self.id,
            "name": self._name,
            "email": self._email,
            # Save each project as a dictionary too
            "projects": [p.to_dict() for p in self.projects]
        }

    @classmethod
    def from_dict(cls, data):
        # Import here to avoid circular imports
        from models.project import Project

        user = cls(data["name"], data["email"])
        user.id = data["id"]

        # Rebuild each project from saved data
        for project_data in data.get("projects", []):
            project = Project.from_dict(project_data)
            user.projects.append(project)

        return user

    def __str__(self):
        project_count = len(self.projects)
        return f"[ID: {self.id}] {self._name} | Email: {self._email} | Projects: {project_count}"

    def __repr__(self):
        return f"User(name={self._name}, email={self._email})"
