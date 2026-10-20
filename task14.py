from contextlib import contextmanager
@contextmanager
def log_operation(path, log_name):
    with open(path, "a", encoding="utf-8") as file:
        file.write(f"START: {log_name}\n")
        try:
            yield
        except BaseException:
            file.write(f"ERROR: {log_name}\n")
            raise
        else:
            file.write(f"END: {log_name}\n")
with log_operation("log.txt", "Calculation"):
    print(2+3)
