import re

logs = [
    "2026-09-24 10:15:32 INFO User 123 logged in",
    "2026-09-24 10:16:04 ERROR User 456 authentication failed",
    "2026-09-24 10:17:21 INFO User 123 opened page",
    "2026-09-24 10:18:45 WARNING User 789 too many requests",
    "2026-09-24 10:19:02 ERROR User 123 database connection failed",
]

pattern = (
    r"(?P<datetime>[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2})"
    r"\s+(?P<level>INFO|WARNING|ERROR)"
    r"\s+User\s+(?P<user_id>[0-9]+)"
    r"\s+(?P<message>.+)"
)
logs_done = []
for line in logs:
    match = re.finditer(pattern, line)
    for group in match:
        logs_done.append(group.groupdict())
print(logs_done)

