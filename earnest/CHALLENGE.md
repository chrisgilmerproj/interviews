# Deriving Fixed Expenses before Education

Your task is to write a program which will take a person's credit report, parse it, and return JSON describing
both the parsed contents of the credit report and some derived facts.

## Credit Report Format

A Credit Report contains a list of tradelines (essentially a list of any loan or available line of credit that a
person has). Each tradeline has a code and subcode which describes the type of liability. For example, all
credit cards have a code of '12', a conventional mortgage has a code of '10' and a subcode of '12'. Each
tradeline also has a monthly payment and a current balance. Some tradelines may not carry a balance - for
example, a fully paid off credit card.

Our credit report input comes in a specific format. Each line represents a tradeline, with the different
properties of the tradeline in a specific order, separated by spaces. The properties are listed in the following
order: reported date, code, subcode, monthly payment, and current balance. For example, the following line
describes a credit card account with a code of 12 and a subcode of 5 reported on May 27, 2015 with a
minimum monthly payment of $120.00 and a current balance of $2,113.12:

```
2015-05-27 12 5 $120.00 $2113.12
```

Monetary values may or may not be prefixed by a dollar sign, and may also sometimes have thousands
separated by commas. They will never have fractional cents.

Any line with an unexpected number of fields can be safely ignored.

## Fixed Expenses Before Education

Your program must calculate a person's Fixed Expenses Before Education based on their credit report. Fixed
Expenses Before Education is defined as:
Non-Housing Expenses + Housing Expenses.

Housing Expense is the sum of monthly payments for all mortgage tradelines, where a mortgage tradeline
has a code of 10 and a subcode of 12 or 15. If the credit report contains no mortgage tradelines, then the
program should assume a housing expense of $1061 (the national average monthly rent).

Non-Housing Expenses is the sum of monthly payments for tradelines which are not mortgages and are not
student loan payments. A student loan tradeline has a code of 5.

Any tradelines with zero current balance should not be considered in this Fixed Expenses calculation.

## Output Format

Your program should output data about each parsed tradeline plus the calculated Fixed Expenses Before
Education in the following format:

```
{
fixed_expenses_before_education: 412321,
tradelines: [
{
type: 'education',
monthly_payment: 34131,
current_balance: 14210021,
},
{
type: 'mortgage',
monthly_payment: 234412,
current_balance: 51232121,
},
{
type: 'other',
monthly_payment: 31241,
current_balance: 4123,
},
{
type: 'mortgage',
monthly_payment: 123012,
current_balance: 21330061,
}
]
}
```

Note that all monetary amounts must be represented in non-fractional cents. For example, $1245.21 must be
represented as 124521.

## Sample Input and Output

For this input:

```
2015-10-10 10 12 $1470.31 $659218.00
2015-10-10 5 1 $431.98 $51028.00
2015-10-09 8 15 $340.12 $21223.20
2015-10-10 10 15 $930.12 $120413.00
2015-10-09 12 5 $150.50 $6421.21
```

the following output is correct:

```
{
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
```
