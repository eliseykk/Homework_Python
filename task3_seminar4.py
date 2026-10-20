import csv
with open("students.csv", "r", encoding="utf-8", newline="") as file:
    groups = {}
    reader = csv.reader(file)
    header = next(reader, None)
    max_score = float("-inf")
    max_score_name = None
    for row in reader:
        if not row:
            continue
        if row[1] in groups:
            groups[row[1]]["total_score"] += int(row[2])
            groups[row[1]]["count"] += 1
        else:
            groups[row[1]] = {"total_score": int(row[2]), "count": 1}
        if int(row[2]) > max_score:
            max_score = int(row[2])
            max_score_name = row[0]
total_score = 0
count = 0
for group, stats in groups.items():
    total_score += groups[group]["total_score"]
    count += groups[group]["count"]
    groups[group]["average_score"] = groups[group]["total_score"] / groups[group]["count"]
if count != 0:
    mean_score = total_score / count
    print(mean_score, max_score_name)
else:
    print("Нет данных о студентах")
for key in groups:
    print(f"{key}: {groups[key]['average_score']}", end=" ")


