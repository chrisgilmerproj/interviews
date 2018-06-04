#! /usr/bin/env python3

import io
import textwrap
import unittest

from fixed_expenses import calculate_fixed_expenses_before_education


class TestFixedExpenses(unittest.TestCase):

    def setUp(self):

        self.expected = {
            "fixed_expenses_before_education": 289105,
            "tradelines": [
                {
                    "type": "mortgage",
                    "monthly_payment": 147031,
                    "current_balance": 65921800
                },
                {
                    "type": "education",
                    "monthly_payment": 43198,
                    "current_balance": 5102800
                },
                {
                    "type": "other",
                    "monthly_payment": 34012,
                    "current_balance": 2122320
                },
                {
                    "type": "mortgage",
                    "monthly_payment": 93012,
                    "current_balance": 12041300
                },
                {
                    "type": "other",
                    "monthly_payment": 15050,
                    "current_balance": 642121
                }
            ]
        }

        self.default_housing_expenses = {'CA': 106100}

    def create_file(self, text):
        open_file = io.StringIO()
        open_file.write(text)
        open_file.seek(0)
        return open_file

    def test_calculate_fixed_expenses_before_education(self):

        expenses = textwrap.dedent("""\
            2015-10-10 10 12 $1470.31 $659218.00
            2015-10-10 5 1 $431.98 $51028.00
            2015-10-09 8 15 $340.12 $21223.20
            2015-10-10 10 15 $930.12 $120413.00
            2015-10-09 12 5 $150.50 $6421.21""")
        open_file = self.create_file(expenses)
        out = calculate_fixed_expenses_before_education(open_file, self.default_housing_expenses)
        self.assertEquals(out, self.expected)
        open_file.close()

    def test_with_commas(self):

        expenses = textwrap.dedent("""\
            2015-10-10 10 12 $1,470.31 $659,218.00
            2015-10-10 5 1 $431.98 $51,028.00
            2015-10-09 8 15 $340.12 $21,223.20
            2015-10-10 10 15 $930.12 $12,0413.00
            2015-10-09 12 5 $150.50 $6,421.21""")
        open_file = self.create_file(expenses)
        out = calculate_fixed_expenses_before_education(open_file, self.default_housing_expenses)
        self.assertEquals(out, self.expected)
        open_file.close()

    def test_without_dollar_signs(self):

        expenses = textwrap.dedent("""\
            2015-10-10 10 12 1470.31 659218.00
            2015-10-10 5 1 431.98 51028.00
            2015-10-09 8 15 340.12 21223.20
            2015-10-10 10 15 930.12 120413.00
            2015-10-09 12 5 150.50 6421.21""")
        open_file = self.create_file(expenses)
        out = calculate_fixed_expenses_before_education(open_file, self.default_housing_expenses)
        self.assertEquals(out, self.expected)
        open_file.close()


if __name__ == '__main__':
    unittest.main()
