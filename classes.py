import os
from pprint import pprint


class Task:
    def __init__(self, task_name, deadline, task_author, task_creation_date, for_whom: list, task_description: str = None):
        self.task_name = task_name
        self.deadline = deadline
        self.task_author = task_author
        self.task_creation_date = task_creation_date
        self.for_whom: list = for_whom
        self.task_description = task_description

    def __str__(self):
        return self.task_name

    async def save_task_to_data(self):
        s: str = ";"
        for person in self.for_whom:
            file_path = os.path.join("data", person)
            content = open(file_path, "r").read().splitlines()
            long_value = self.task_name + s + self.deadline + s + self.task_creation_date + s + self.task_author
            if self.task_description:
                long_value += "$" + self.task_description
            content.append(long_value)
            content = "\n".join(content)
            with open(file_path, "w") as f:
                f.write(content)
                print("content")
                pprint(content)
                print("Person")
                pprint(file_path)

    def reconstruct(self, task_dictionary: dict[str: str, list[str]]):
        self.__init__(task_dictionary["task_name"], task_dictionary["task_deadline"], task_dictionary["task_author"],
                      task_dictionary["task_creation_date"], task_dictionary["for_whom"], task_dictionary["task_description"])
        return self
