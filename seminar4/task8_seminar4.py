def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            read = file.read()
    except FileNotFoundError as error:
        print(f"Файл не найден! Ошибка: {error}")
        return None
    except PermissionError as error:
        print(f"Недостаточно прав! Ошибка: {error}")
        return None
    except IsADirectoryError as error:
        print(f"Это каталог, а не файл! Ошибка {error}")
        return None
    except NotADirectoryError as error:
        print(f"Часть пути не является каталогом! Ошибка: {error}")
        return None
    except UnicodeDecodeError as error:
        print(f"Ошибка декодировки! Ошибка: {error}")
        return None
    except OSError as error:
        print(f"Ошибка операционной системы! Ошибка: {error}")
        return None
    else:
        return read
