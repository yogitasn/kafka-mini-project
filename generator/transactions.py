# generator/transactions.py
from random import choices, randint
from string import ascii_letters, digits

def _random_account_id():
    account_chars: str = digits + ascii_letters
    """ Return a random account number made of 12 characters."""
    acc_no ="".join(choices(account_chars, k=12))
    return acc_no

def _random_amount():
    """ Return a random amount between 1.00 and 1000.00."""
    random_amt = (randint(100, 1000000))/100
    return random_amt

def create_random_transaction():
    """ Create a fake, randomised transaction."""
    return {
         "source": _random_account_id(),
         "target": _random_account_id(),
         "amount": _random_amount(),
         # Keep it simple: it's all dollars
         "currency": "USD"
        }
