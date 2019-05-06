from itertools import cycle

from ai import AI
from board import Board
from player import Player


class Engine:
    def __init__(self):
        self.board = Board()

        self.player1 = Player('halo1', self.board, 'white')
        self.player2 = Player('halo2', self.board, 'black')

        self.queue = cycle([self.player1, self.player2])
        self.current_player = None
        self.next_round()

    def next_round(self):
        self.current_player = next(self.queue)

    def handle_touch(self, field_id):
        if field_id in self.board.fields:
            if not isinstance(self.current_player, AI):
                if self.current_player.handle_touch(field_id):
                    self.next_round()
                return True
        return False
