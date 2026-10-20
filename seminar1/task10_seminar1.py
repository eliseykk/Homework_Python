import json
import logging
import time
from dataclasses import dataclass
from datetime import date, timedelta
from functools import wraps
from pathlib import Path


def operation_time(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return function(*args, **kwargs)
        finally:
            end = time.perf_counter()
            logging.getLogger("task10").info("%s: %.6f секунд", function.__name__, end - start)
    return wrapper


@dataclass
class Task:
    name: str
    priority: int
    status: str
    due_date: str

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Название задачи не должно быть пустым")
        self.name = self.name.strip()
        if type(self.priority) != int or not 1 <= self.priority <= 3:
            raise ValueError("Приоритет должен быть числом от 1 до 3")
        if self.status not in ("new", "in_progress", "done"):
            raise ValueError("Неизвестный статус задачи")
        if not isinstance(self.due_date, str):
            raise ValueError("Срок нужно передать строкой YYYY-MM-DD")
        self.due_date = date.fromisoformat(self.due_date).isoformat()


class TaskManager:
    def __init__(self):
        self.tasks = []

    @operation_time
    def find_task(self, name):
        for task in self.tasks:
            if task.name.casefold() == name.strip().casefold():
                return task
        return None

    @operation_time
    def add_task(self, task):
        if not isinstance(task, Task):
            raise TypeError("Нужно передать объект Task")
        if self.find_task(task.name) is not None:
            raise ValueError("Задача с таким названием уже есть")
        self.tasks.append(task)

    @operation_time
    def remove_task(self, name):
        task = self.find_task(name)
        if task is None:
            raise ValueError("Задача не найдена")
        self.tasks.remove(task)

    @operation_time
    def change_status(self, name, new_status):
        if new_status not in ("new", "in_progress", "done"):
            raise ValueError("Неизвестный статус задачи")
        task = self.find_task(name)
        if task is None:
            raise ValueError("Задача не найдена")
        task.status = new_status

    @operation_time
    def get_high_priority(self):
        high_tasks = []
        for task in self.tasks:
            if task.priority == 3:
                high_tasks.append(task)
        return high_tasks

    @operation_time
    def get_overdue(self, today=None):
        if today is None:
            today = date.today()
        overdue_tasks = []
        for task in self.tasks:
            if date.fromisoformat(task.due_date) < today and task.status != "done":
                overdue_tasks.append(task)
        return overdue_tasks

    @operation_time
    def save_tasks(self, path):
        data = []
        for task in self.tasks:
            data.append({
                "name": task.name,
                "priority": task.priority,
                "status": task.status,
                "due_date": task.due_date,
            })
        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            logging.getLogger("task10").error("Ошибка сохранения: %s", error)
            print(f"Не удалось сохранить задачи: {error}")
            return False
        return True

    @operation_time
    def load_tasks(self, path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("В JSON должен находиться список задач")

            new_tasks = []
            names = set()
            for item in data:
                if not isinstance(item, dict):
                    raise ValueError("Каждая задача должна быть словарём")
                task = Task(item["name"], item["priority"], item["status"], item["due_date"])
                if task.name.casefold() in names:
                    raise ValueError("В файле повторяются названия задач")
                names.add(task.name.casefold())
                new_tasks.append(task)
        except (OSError, UnicodeDecodeError, ValueError, TypeError, KeyError) as error:
            logging.getLogger("task10").error("Ошибка загрузки: %s", error)
            print(f"Не удалось загрузить задачи: {error}")
            return False

        # Заменяем список только после успешной проверки всего файла.
        self.tasks = new_tasks
        return True


if __name__ == "__main__":
    folder = Path(__file__).resolve().parent
    logging.basicConfig(
        filename=folder / "task10.log",
        encoding="utf-8",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )
    manager = TaskManager()
    today = date.today()
    manager.add_task(Task("Лабораторная", 3, "new", (today - timedelta(days=1)).isoformat()))
    manager.add_task(Task("Повторить Python", 2, "new", (today + timedelta(days=3)).isoformat()))
    manager.add_task(Task("Прочитать главу", 1, "done", (today - timedelta(days=2)).isoformat()))
    manager.change_status("Лабораторная", "in_progress")

    print("Высокий приоритет:")
    for task in manager.get_high_priority():
        print(task)
    print("Просроченные задачи:")
    for task in manager.get_overdue():
        print(task)

    # Демонстрация сохраняется отдельно от пользовательского tasks.json.
    path = folder / "tasks_demo.json"
    if manager.save_tasks(path):
        loaded_manager = TaskManager()
        if loaded_manager.load_tasks(path):
            print("Загруженные задачи:")
            for task in loaded_manager.tasks:
                print(task)
            loaded_manager.remove_task("Прочитать главу")
            print("После удаления:", len(loaded_manager.tasks))
