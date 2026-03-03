# This file handles saving and loading data to/from a JSON file

import json   
import os     

DATA_FILE = "data/data.json"


def ensure_data_folder():
   
    if not os.path.exists("data"):
        os.makedirs("data")


def save_data(users):
    
    ensure_data_folder()

    # Convert each User object into a dictionary
    # JSON can only store basic types: strings, numbers, lists, dicts
    data = [user.to_dict() for user in users]

    # Open the file and write the JSON data
    # 'w' means write mode (creates file if it doesn't exist)
    # indent=2 makes the JSON pretty and readable
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=2)

    print(f"Data saved to {DATA_FILE}")


def load_data():
   
    from models.user import User

    # If the file doesn't exist yet, return an empty list
    if not os.path.exists(DATA_FILE):
        return []

    # try-except catches errors so the program doesn't crash
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        # Convert each dictionary back into a User object
        users = [User.from_dict(user_data) for user_data in data]

        # Fix the ID counters so new objects don't get duplicate IDs
        _sync_id_counters(users)

        return users

    except json.JSONDecodeError:
        print("Warning: Data file is corrupted. Starting fresh.")
        return []
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


def _sync_id_counters(users):
  
    from models.user import User
    from models.project import Project
    from models.task import Task

    max_user_id = 0
    max_project_id = 0
    max_task_id = 0

    for user in users:
        if user.id > max_user_id:
            max_user_id = user.id

        for project in user.projects:
            if project.id > max_project_id:
                max_project_id = project.id

            for task in project.tasks:
                if task.id > max_task_id:
                    max_task_id = task.id

    # Set counters to max + 1 so next ID is unique
    User._id_counter = max_user_id + 1
    Project._id_counter = max_project_id + 1
    Task._id_counter = max_task_id + 1
