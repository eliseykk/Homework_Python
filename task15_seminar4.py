from io import StringIO
def count_lines(stream):
    counter = 0
    for line in stream:
        counter += 1
    return counter
