#!/usr/bin/env python3

# Board Game
ROW = 6
COL = 7

# How many connections needed
CONNECT = 4

COLORS = ['red', 'blue']


class GameState(object):
    def __init__(self, row, col, *players):
        self.row = row
        self.col = col
        self.players = players

        # Generate board? Fill in as go?
        self.board = []
        for i in range(0, col):
            self.board.append([])

# [
#   [r. b. r. r. r ],  # if full return error
#   [ ],
#   [ ],
#   [ ],
#   [ ],
#   [ ],
#   [ ],
#   [ ],
# ]

    def is_connected(self, row, col, color):
        pass

    def print_board(self):
        pass

    def place_piece(self, col, color):
        filled = len(self.board[col])
        if filled == self.col:
            raise Exception
        self.board[col].append(color)
        return filled

    def ask_user(self, user):
        if user.is_ai:
            return user.check_board(self.board)
        else:
            return int(input('Which column? '))

    def play(self):

        winner_found = False
        while not winner_found:
            for user in self.players:
                # ask player
                # loop if exception raised
                col = self.ask_user(user)
                row = self.place_piece(col, user.color)
                if self.is_connected(row, col, user.color):
                    winner_found = True
                    break
                else:
                    continue


class User(object):

    def __init__(self, name, color, is_ai=False):
        pass

    def check_board(self, board):
        pass


def main():
    player1 = User('chris', 'blue')
    player2 = User('ken', 'red')

    game_state = GameState(ROW, COL, player1, player2)


if __name__ == "__main__":
    main()
