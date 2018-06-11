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


import pprint


def create_balances(transactions):
    # {Sarah: 300, John: -100, Alice: -100, Bob: -100}
    balance = {
    }
    for transaction in transactions:
        owner = transaction['owner']
        users = transaction['users']
        amount = transaction['amount']
        ind_amount = amount / len(users)

        if owner in balance:
            balance[owner] += amount
        else:
            balance[owner] = amount

        for user in users:
            if user in balance:
                balance[user] -= ind_amount
            else:
                balance[user] = -ind_amount
    return balance


def create_transactions(balances):
    transactions = []
    for from_person, from_amount in balances.items():
        for to_person, to_amount in balances.items():
            if from_person == to_person:
                continue
            if from_amount < 0 and to_amount > 0:
                transaction.append(from_person, to_person, to_amount - from_amount)
    return transactions


if __name__ == "__main__":
    transactions = [
        {'owner': 'Sarah',
         'amount': 400.0,
         'users': ['Alice', 'John', 'Bob', 'Sarah']},
        {'owner': 'John',
         'amount': 100.0,
         'users': ['Alice', 'Bob']},
    ]
    balances = create_balances(transactions)
    owes = create_transactions(balances)
    pprint.pprint(owes)
