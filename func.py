import os.path
from time_manager import get_time
from classes import Task


async def create_user(name, creator) -> str:
    try:
        if not os.path.exists(os.path.join("data/", name)):
            new_file = open(os.path.join("data/", name), "w")
            new_file.write(get_time() + ";" + creator + "\n")
            return f"User '{name}' has been created"
        else:
            return "User already exists"
    except Exception as e:
        if str(e) != "substring not found":
            return "Error: " + str(e)
        else:
            os.remove(os.path.join("data/", name))
            return "Error: " + str(e)


async def add_task(task_name, deadline, task_author, task_creation_date, description, for_whom):
    new_task = Task(task_name, deadline, task_author, task_creation_date, description, for_whom)
    try:
        new_task.save_task_to_data()
        return f"Task: '{task_name}' successfully saved for user: '{for_whom}'."
    except FileNotFoundError:
        return f"User '{for_whom}' not found. Try using the 'list_users' command."  # TODO: add the list-users command

def format_time(time_string):
    return time_string
