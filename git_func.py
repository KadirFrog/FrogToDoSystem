from github import Github
from git_credentials_manager import *
from time_manager import get_time
import base64
from github import InputGitTreeElement

todo_adder = ""  # display username of the person updating the TODO

def get_file_content() -> str:
    github_instance = Github(get_git_username(), get_git_password())
    user = github_instance.get_user()
    repository = user.get_repo(get_git_repository())
    file_content = repository.get_contents(get_git_file_name())
    print("File Read:" + file_content.decoded_content.decode())  # Debug line (removable)
    return file_content.decoded_content.decode()

def write_to_file(new_file_content: str) -> None:  # "new_file_content" contains the whole text meaning everything in the file will be deleted before writing it into git
    g = Github(get_git_username(), get_git_password())
    repo = g.get_user().get_repo(get_git_repository())
    file_content = repo.get_contents(get_git_file_name())
    commit_message = f"{get_time()}: Commit by " + todo_adder
    repo.update_file(file_content.path, commit_message, new_file_content, file_content.sha)
    