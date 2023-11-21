import os.path
from typing import List

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
        os.remove(os.path.join("data/", name))
        await error_log(str(e), creator)
        return "Error: " + str(e)


async def add_task(task_name, deadline, task_author, task_creation_date, for_whom):
    new_task = Task(task_name, deadline, task_author, task_creation_date, for_whom)
    try:
        new_task.save_task_to_data()
        return f"Task: '{task_name}' successfully saved for user: '{for_whom}'."
    except FileNotFoundError:
        return f"User '{for_whom}' not found. Try using the 'list_users' command."  # TODO: add the list-users command


def format_time(time_string):
    return time_string


async def add_description_to_task(task_name, description, giver):
    try:
        global final_return_message
        for filename in os.listdir("data"):
            file_path = os.path.join("data", filename)
            content = open(file_path, "r").read().splitlines()
            final_return_message = []
            for x in range(len(content)):
                line = content[x]
                task_name_of_line = line[: line.index(";")]
                if task_name_of_line == task_name:
                    try:
                        content[x] = content[x][:content[x].index("$")]
                    except:
                        ""
                    content[x] += "$" + description
                    final_return_message.append(
                        f"Description added to task: '{task_name_of_line}' at user: '{filename}'.")

                with open(file_path, "w") as f:
                    f.write("\n".join(content))

        return f"Description:\n'{description}'\n" + "\n".join(final_return_message)

    except Exception as e:
        await error_log(str(e), giver)
        return "Error: " + str(e)


async def delete_user(user_name, deleter):
    try:
        os.remove(os.path.join("data", user_name))
        s: str = ";"
        content = open("other_data/deletions", "r").read().splitlines()
        content.append(get_time() + s + user_name + s + deleter + s)
        with open("other_data/deletions", "w") as f:
            f.write("\n".join(content))
        return f"User '{user_name}' has been deleted."
    except Exception as e:
        await error_log(str(e), deleter)
        return f"Error: {e}"


async def error_log(error: str, error_causer: str):
    s: str = ";"
    content = open("other_data/error_logs", "r").read().splitlines()
    content.append(get_time() + s + error + s + error_causer + s)
    with open("other_data/error_logs", "w") as f:
        f.write("\n".join(content))


def task_format(task_save_format_data):
    task_save_format_data, description = task_save_format_data.split("$")
    task_name, task_deadline, task_creation_date, task_author = task_save_format_data.split(";")
    return \
        f"""{task_name}
|   Beschreibung: '{description}'
|   Deadline: {task_deadline}
|   Aufgabe erstellt von: '{task_author}'
|   Aufgabe erstellt am: {task_creation_date}

"""


async def show_tasks(user_name, requester):
    try:
        content = open(os.path.join("data", user_name), "r").read().splitlines()[1:]
        final_output = []
        for line in content:
            final_output.append(task_format(line))
        return f"Aufgaben von '{user_name}'\n" + "\n".join(final_output)

    except Exception as e:
        await error_log(str(e), requester)
        return f"Error: {e}"