import re
def is_valid_login(login: str):
    if len(login) < 4 or len(login) > 16:
        print("Login must has 4-16 symbols")
        return False
    if re.fullmatch(r"^[A-Za-z][A-Za-z0-9_]+", login):
        return True
    else:
        return False
print(is_valid_login("Aяasd"))