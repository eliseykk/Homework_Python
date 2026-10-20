def parse_number(value):
    return float(value)
try:
    parse = parse_number(input())
    print(parse)
except ValueError:
    print("ValueError!!")
