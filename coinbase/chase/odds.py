#!/usr/bin/env python3


def odds():
    count = 1
    while True:
        yield count
        count += 2


def evens():
    for odd in odds():
        yield odd + 1


def negatives(gen):
    for g in gen:
        yield -1 * g


def interleave(*gen_list):
    while True:
        for g in gen_list:
            yield next(g)


if __name__ == "__main__":
    # for i in interleave(odds(), evens()):
    #     print(i)
    # for i in interleave(negatives(odds()), negatives(evens())):
    #     print(i)
    # for i in negatives(interleave(odds(), evens())):
    #     print(i)
    # for i in interleave(interleave(odds(), evens()), negatives(interleave(odds(), evens()))):
    #     print(i)
    for i in interleave(odds(), negatives(odds()), evens(), negatives(evens())):
        print(i)
