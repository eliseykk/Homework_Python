import re

products = [
    "PRD-12345",
    "PRD-00123",
    "USR-12345",
    "PRD-987",
    "PRD-ABCDE",
    "PRD-54321"
]
good_products = []
for line in products:
    match = re.fullmatch(r"PRD-[0-9]{5}", line)
    if match:
        good_products.append(line)
print(good_products)
