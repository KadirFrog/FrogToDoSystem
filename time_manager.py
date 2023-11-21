import datetime
def get_time() -> str:
    a = datetime.datetime.now().date()
    a = str(a)
    return a
