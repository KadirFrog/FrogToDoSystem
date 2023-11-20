import os.path
from time_manager import get_time

async def create_user(name, creator) -> str:
    try:
        if not os.path.exists(os.path.join("data/", name)):
            new_file = open(os.path.join("data/", name), "w")
            new_file.write(get_time() + ";" + creator + "\n")
            return f"User '{name}' has been created"
        else:
            return "User already exists"
    except Exception as e:
        return "Error: " + str(e)
