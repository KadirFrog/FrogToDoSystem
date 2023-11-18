import datetime
def get_time() -> str:
    a = datetime.datetime.now().time()
    a = str(a)
    a = a[:a.index(".")]
    return a
