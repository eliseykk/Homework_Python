import random
from functools import wraps


def retry(attempts):
    if type(attempts) != int or attempts <= 0:
        raise ValueError("Количество попыток должно быть положительным целым числом")

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for attempt in range(attempts):
                try:
                    return function(*args, **kwargs)
                except Exception as error:
                    print(f"Попытка {attempt + 1}: {error}")
                    if attempt == attempts - 1:
                        raise
        return wrapper
    return decorator


@retry(3)
def load_data():
    """Загружает данные; случайная ошибка имитирует сбой соединения."""
    if random.random() < 0.6:
        raise ConnectionError("Не удалось загрузить данные")
    return {"name": "Nina", "score": 85}


if __name__ == "__main__":
    print("Имя функции:", load_data.__name__)
    try:
        data = load_data()
    except ConnectionError as error:
        print(f"Попытки закончились: {error}")
    else:
        print("Данные получены:", data)
