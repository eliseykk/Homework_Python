from pathlib import Path
path = "sample_directory"
directory = Path(path)
counter_files = 0
counter_directory = 0
total_size_files = 0
for entry in directory.iterdir():
    if entry.is_file():
        counter_files += 1
        total_size_files += entry.stat().st_size
    elif entry.is_dir():
        counter_directory += 1
py_files = [entry for entry in directory.glob("*.py") if entry.is_file()]
print(counter_files, counter_directory, total_size_files, py_files)

