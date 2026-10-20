import csv
with open("text.csv", "r", encoding="utf-8", newline="") as file:
    reader = csv.DictReader(file)
    header = reader.fieldnames
    load = []
    for line in reader:
        if float(line['price']) > 100:
            load.append(line)
with open("expensive.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=header or ["name", "category", "price"])
    writer.writeheader()
    writer.writerows(load)
