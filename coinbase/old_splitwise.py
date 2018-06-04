#! /usr/bin/env python3


"""
Sarah rents a car for the trip - she pays $400 for the car, which is used by Alice, John, Bob and herself.
Later in the trip, John went out and bought groceries for $100, which was used only by Alice and Bob.

Now, the trip is over and everyone wants to get paid back what they are owed - print out the list of
transactions that would settle everyone's debts.

output:
    John -> Sarah: $100
    Bob -> Sarah: $100
    Alice -> Sarah: $100
    Alice -> John $50
    Bob -> John $50

output optimized:
    Alice -> Sarah: $150
    Bob -> Sarah: $150
"""


from collections import defaultdict
import pprint


def create_transactions(transactions):
    # John: {Sarah: 100}
    # Alice: {John: 25}
    owes = {
    }
    for transaction in transactions:
        owner = transaction['owner']
        users = transaction['users']
        amount = transaction['amount'] / len(users)
        for user in users:
            if user == owner:
                continue
            if user in owes:
                owes[user][owner] += amount
            else:
                owes[user] = defaultdict(int)
                owes[user][owner] = amount
    return owes


def simplify_transactions(owes):
    owes_2 = {}
    for owe, transactions in owes.items():
        for person, amount in transactions.item():
            pass
    return owes_2


def format_transactions(owes):
    out = []
    for owe, transactions in owes.items():
        for person, amount in transactions.items():
            out.append("{0} -> {1} {2}".format(owe, person, amount))
    return '\n'.join(out)


if __name__ == "__main__":
    transactions = [
        {'owner': 'Sarah',
         'amount': 400.0,
         'users': ['Alice', 'John', 'Bob', 'Sarah']},
        {'owner': 'John',
         'amount': 100.0,
         'users': ['Alice', 'Bob']},
    ]
    owes = create_transactions(transactions)
    owes = simplify_transactions(owes)
    ftrans = format_transactions(owes)
    pprint.pprint(ftrans)
