import re
with open("logs.txt", "r", encoding="utf-8") as file:
    id_users = []
    error_str = []
    error_id_users = []
    for line in file:
        id_users.extend(re.findall(r"\bUser\s+([0-9]+)\b", line))
        if re.findall(r"\bERROR\b", line):
            error_str.append(line.rstrip("\n"))
            error_id_users.extend(re.findall(r"\bUser\s+([0-9]+)\b", line))
print(id_users)
print(error_str)
print(error_id_users)

