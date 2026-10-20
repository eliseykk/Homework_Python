import re
with open("emails.txt", "r", encoding="utf-8") as file:
    emails = []
    for line in file:
        find_email = re.findall(r"[A-Za-z0-9_+.-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\b", line)
        if find_email:
            emails.extend(find_email)
    emails = list(dict.fromkeys(emails))
print(emails)

