#! /usr/bin/env python3


def interleave(a, store):
    chase = True
    while chase:
        chase = False
        for l in a:
            if len(l):
                store.append(l.pop(0))
                if len(l):
                    chase = True


if __name__ == "__main__":
    store = []
    a = [[1, 2, 3], [4, 5], [6], [], [7, 8, 9]]
    interleave(a, store)
    print(store)
