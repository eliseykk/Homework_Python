import re

with open("task20.txt","r",encoding="utf-8") as file:
    read = file.read()
    date_list = re.findall(r"\b[0-9]{2}\.[0-9]{2}\.[0-9]{4}\b", read)
print(date_list)
