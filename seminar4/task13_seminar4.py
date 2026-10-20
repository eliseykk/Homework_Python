import time
from contextlib import contextmanager

class Timer():
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        self.times = self.end - self.start
        print(f"Время выполнения: {self.times}")
        return False
def some_function():
    print("Бебебе")
    print("Бубубу")
    print("Каэйнжелбох")
with Timer():
    some_function()

#VARIANT 2

@contextmanager
def timer():
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"Время выполнения: {end - start}")
with timer():
    some_function()
