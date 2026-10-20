from pathlib import Path

path = input("Введите путь: ")
directory = Path(path)
if not(directory.is_dir()):
    print("Указан неверный путь!")
    exit()
extension = input("Введите расширение: ").strip().lstrip(".")
extension_files = []
for entry in directory.rglob(f"*.{extension}"):
    if entry.is_file():
        extension_files.append({'path': entry.resolve(), 'size': entry.stat().st_size})
for entry in extension_files:
    print(f"{entry['path']}: {entry['size']} байт")
if not extension_files:
    print("Файлы не найдены")
