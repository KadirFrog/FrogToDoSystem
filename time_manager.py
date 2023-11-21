import datetime
def get_time() -> str:
    a = datetime.datetime.now().date()
    a = ".".join(str(a).split("-")[::-1])
    return a
