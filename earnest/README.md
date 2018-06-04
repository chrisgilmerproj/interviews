# Earnest Coding Challenge

## Quick Start

This program was written and tested in python3

```
$ ./fixed_expenses.py
```

or

```
$ python3 fixed_expenses.py
```

## Testing

```
$ ./test_fixed_expenses.py
```

or

```
$ python3 test_fixed_expenses.py
```

# Design Decisions

## Regex for line parsing

This was chosen so that I could easily skip bad input and more quickly turn each line into parsed data.

## Passing File-like Objects

I chose to pass a file-like object into the method because it facilitates testing.  It also means
I can put the file opening and exception logic outside of the function I wish to test.

## Codes

I put the codes in dictionary structures to speed up lookup.  I can update this format in the future
to hold more codes and subcodes.  I could even further change this structure to include
names based on the code/subcode lookup.

## Working with integers

The document made it very clear that we'll be working with integers.  So before doing other work the
parsed data is transformed to ensure the currency amounts are in cents.  I've done this in a separate method
which can be modified later.

## Returning python datatype

I leave the final translation of the data to JSON up to the user.  This helps simplify testing and allows
us to pass the data into other utilities without having to re-transform.
