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
        os.remove(os.path.join("data/", name))
        await error_log(str(e), creator)
        return "Error: " + str(e)


async def add_task(task_name, deadline, task_author, task_creation_date, for_whom):
    new_task = Task(task_name, deadline, task_author, task_creation_date, for_whom)
    if len(for_whom) == 1:
        s = "D"
    else:
        s = "Einer d"
    try:
        new_task.save_task_to_data()
        return f"Aufgabe: '{task_name}' erfolgreich gespeichert user: '{for_whom}'."
    except FileNotFoundError:
        return f"{s}er Benutzer '{for_whom}' wurde nicht gefunden. Du kannst den 'list-users' command benutzen um die usernames von allen usern zu sehen."


def format_time(time_string):
    return time_string


async def add_description_to_task(task_name, description, requester):
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
        await error_log(str(e), requester)
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
    try:
        s: str = ";"
        content = open("other_data/error_logs", "r").read().splitlines()
        content.append(get_time() + s + error + s + error_causer + s)
        with open("other_data/error_logs", "w") as f:
            f.write("\n".join(content))
    except Exception as e:
        print("System Failure: " + str(e))


def task_format(task_save_format_data):
    try:
        task_save_format_data, description = task_save_format_data.split("$")
    except:
        description = "Keine"
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
        if final_output:
            return f"Aufgaben von '{user_name}'\n" + "\n".join(final_output)
        else:
            return f"User: '{user_name}' hat keine Aufgaben."

    except Exception as e:
        await error_log(str(e), requester)
        return f"Error: {e}"


async def task_done(task_name, requester):
    final_return_message_task_done = []
    for filename in os.listdir("data"):
        filepath = os.path.join("data", filename)
        content = open(filepath, "r").read().splitlines()
        for x in range(len(content)):
            read_task_name = content[x][: content[x].index(";")]
            if read_task_name == task_name:
                try:
                    content[x] = content[x].split("$")
                    content[x][0] = content[x][0].split(";")
                    content[x][0][-1] = filename
                    content[x][0].append(";" + requester)
                    content[x][0] = ";".join(content[x][0])
                    content[x] = "$".join(content[x])
                except Exception as e:
                    print(e)
                    content[x] = content[x].split(";")
                    content[x][-1] = filename
                    content[x].append(";" + requester)
                    content[x] = ";".join(content[x])
                done_content = open("other_data/done", "r").read().splitlines()
                done_content.append(content[x])
                done_content = "\n".join(done_content)
                del content[x]
                with open("other_data/done", "w") as f:
                    f.write(done_content)
                with open(filepath, "w") as f:
                    f.write("\n".join(content))
                final_return_message_task_done.append(
                    f"Aufgabe: '{read_task_name}' wurde für user: '{filename}' als erledigt gespeichert.")
                return "".join(final_return_message_task_done)


async def recently_done(requester, how_many):  # Doesn't support a too high input of how many
    try:
        how_many = int(how_many)
        content = open("other_data/done", "r").read().splitlines()[:how_many]
        if how_many > len(content):
            not_enough: bool = True
        else:
            not_enough: bool = False
        final_return_message_recently_done = ["Letztens Erledigte Aufgaben\n\n"]
        for line in content:
            tl = line.split(";")
            if "" in tl:
                tl.remove("")

            try:
                tl.append(tl[-1].split("$")[1])
                tl[-2] = tl[-2][: tl[-2].index("$")]
            except Exception as e:
                tl.append("Keine")

            task_name, deadline, done_when, task_of, set_done_by, description = tl
            m = \
                f"""Aufgabe: {task_name}
    |   Aufgabe von: {task_of}
    |   Erledigt am: {done_when}
    |   Erklärung: {description}
    |   Deadline: {deadline}
    |   Erledigt gekennzeichnet von: {set_done_by}
    
    """
            final_return_message_recently_done.append(m)

        if not_enough:
            final_return_message_recently_done.append(f"Es werden nur {len(final_return_message_recently_done) - 1} erledigte Aufgaben angezeigt, da noch nicht so viele Aufgaben erledigt wurden. Mensch Yanis!")

        return "".join(final_return_message_recently_done)

    except Exception as e:
        await error_log(str(e), requester)
        return "Error: " + str(e)

def get_all_usernames(requester):
    try:
        a = os.listdir("data/")
        if not a:
            return "Niemand benutzt mich ):"
        a[0] = "- " + a[0]
        return "\n- ".join(a)
    except Exception as e:
        error_log(str(e), requester)
        return f"Error: {e}"
