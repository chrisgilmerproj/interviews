#! /usr/bin/env python3

import json
import re

RE_TRANS = r'^' \
    '(?P<reported_date>[\d]{4}-[\d]{2}-[\d]{2})\s+' \
    '(?P<code>[\d]{1,2})\s+' \
    '(?P<subcode>[\d]{1,2})\s+' \
    '\$?(?P<monthly_payment>[\d\.,]*)\s+' \
    '\$?(?P<current_balance>[\d\.,]*)\s*' \
    '$'

HOUSING_CODES = {
    10: [12, 15],
}

NON_HOUSING_CODES = {
    5: [],
}


def get_default_housing_expenses(filename='housing_expenses.csv'):
    default_housing_expenses = {}
    with open(filename, 'r') as f:
        for line in f:
            state, expenses = line.split(',')
            default_housing_expenses[state] = expenses
    return default_housing_expenses


def monetary_string_to_int(value):
    return int(float(value.replace(',', '')) * 100)


def calculate_fixed_expenses_before_education(open_file, default_housing_expenses, state='CA'):
    re_expenses = re.compile(RE_TRANS)

    fixed_expenses_before_education = 0
    tradelines = []
    mortgage_tradeline_found = False

    for line in open_file:
        transaction = line.strip()
        re_result = re_expenses.match(transaction)
        if re_result:
            parsed_transaction = re_result.groupdict()

            # Default transaction type
            transaction_type = "other"

            # Pull out data
            reported_date = parsed_transaction.pop('reported_date')  # noqa
            code = int(parsed_transaction.pop('code'))
            subcode = int(parsed_transaction.pop('subcode'))

            # Normalize data
            parsed_transaction['monthly_payment'] = monetary_string_to_int(parsed_transaction['monthly_payment'])
            parsed_transaction['current_balance'] = monetary_string_to_int(parsed_transaction['current_balance'])

            # Skip any tradelines with zero current balance
            if parsed_transaction['current_balance'] == 0:
                continue

            # Based on code and subcode modify expenses and change type
            if code in HOUSING_CODES and subcode in HOUSING_CODES[code]:
                mortgage_tradeline_found = True
                fixed_expenses_before_education += parsed_transaction['monthly_payment']
                transaction_type = "mortgage"
            elif code in NON_HOUSING_CODES:
                transaction_type = "education"
            else:
                fixed_expenses_before_education += parsed_transaction['monthly_payment']

            # Add the transaction to the tradeline list
            parsed_transaction.update({"type": transaction_type})
            # tradelines.append(parsed_transaction)

    # Account for missing mortgage transaction
    if not mortgage_tradeline_found:
        fixed_expenses_before_education += default_housing_expenses[state]

    # Return data in json format
    return {
        "fixed_expenses_before_education": fixed_expenses_before_education,
        "tradelines": tradelines,
    }


if __name__ == "__main__":
    state = 'CA'
    filename = 'expenses.txt'
    filename = 'hello.txt'
    default_housing_expenses = get_default_housing_expenses()
    with open(filename, 'r') as open_file:
        out = calculate_fixed_expenses_before_education(open_file, default_housing_expenses, state)
        print(json.dumps(out))
