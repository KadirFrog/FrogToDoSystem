import os


class Task:
    def __init__(self, task_name, deadline, task_author, task_creation_date, for_whom):
        self.task_name = task_name
        self.deadline = deadline
        self.task_author = task_author
        self.task_creation_date = task_creation_date
        self.for_whom = for_whom

    def __str__(self):
        return self.task_name

    def save_task_to_data(self):
        s: str = ";"
        file_path = os.path.join("data", self.for_whom)
        content = open(file_path, "r").read().splitlines()
        content.append(self.task_name + s + self.deadline + s + self.task_creation_date + s + self.task_author)
        content = "\n".join(content)
        with open(file_path, "w") as f:
            f.write(content)
