import re
users_error = []
info_counter = 0
warning_counter = 0
error_counter = 0
with open("task16.txt", "r", encoding="utf-8") as file:
    for line in file:
        readline = re.findall(r"^\S+ \S+ (INFO|ERROR|WARNING)\b", line)
        match readline:
            case ['INFO']:
                info_counter += 1
            case ['ERROR']:
                error_counter += 1
                users_error.extend(re.findall(r"User ([0-9]+)", line))
            case ["WARNING"]:
                warning_counter += 1
print(f"INFO: {info_counter}"
      f"\nERROR: {error_counter}"
      f"\nWARNING: {warning_counter}"
      f"\nUsers_error: {users_error}")
