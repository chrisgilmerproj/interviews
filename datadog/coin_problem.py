'''
Given a number of cents, write a function to make change with the fewest number of coins, returning the number of coins for each denomination needed for the given number of cents.

The coins can be of the standard U.S. denominations: (1, 5, 10, 25).

Example: make_change(33) -> (3, 1, 0, 1)

33 cents = 3*1 + 1*5 + 0*10 + 1*25
'''

# DENOMINATIONS = (1, 5, 10, 25)
DENOMINATIONS = (25, 10, 5, 1)


def make_change(cents, denominations=DENOMINATIONS):
    
    change = []
    current_total = cents
    
    for denom in denominations:
        num_denom = current_total // denom
        if num_denom > 0:
            current_total -= num_denom * denom
        change.append(num_denom)

    return change, current_total


# assert(make_change(33) == [3, 1, 0, 1])

print(make_change(33.5))
print(make_change(75))
print(make_change(1))
print(make_change(101))
print(make_change(100000001))
print(make_change(0))

# print(make_change(-1))
# print(make_chnage('lizard'))
