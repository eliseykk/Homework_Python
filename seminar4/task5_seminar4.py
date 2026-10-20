import json
with open("students.json", "r", encoding="utf-8") as file:
    max_score = float("-inf")
    max_score_student = ""
    load = json.load(file)
    for dictionary in load:
        if dictionary['score'] > max_score:
            max_score = dictionary['score']
            max_score_student = dictionary['name']
        if dictionary['score'] >= 60:
            dictionary['passed'] = True
        else:
            dictionary['passed'] = False
if load:
    print(f"Студент с максимальным баллом: {max_score_student}")
else:
    print("Нет данных о студентах")
with open("new_text.json", "w", encoding="utf-8") as file:
    json.dump(load, file, ensure_ascii=False, indent=4)
