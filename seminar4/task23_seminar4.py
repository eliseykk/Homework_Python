import re
text = "Это   строка    с     большим    количеством   пробелов."
good_text = re.sub(r"\s+", " ", text).strip()
print(good_text)
text = "   Текст   с   пробелами   "
good_text = re.sub(r"\s+", " ", text).strip()
print(good_text)
