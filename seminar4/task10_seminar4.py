class BankError(Exception):
    pass
class InsufficientFundsError(BankError):
    pass
class AccountBlockedError(BankError):
    pass
class InvalidAmountError(BankError):
    pass

def withdraw(balance, amount):
    if amount <= 0:
        raise InvalidAmountError()
    elif amount > balance:
        raise InsufficientFundsError()
    else:
        return (balance - amount)

