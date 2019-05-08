from itertools import cycle

from board import Board
from player import PlayerHuman


class Engine:
    def __init__(self):
        self.board = Board()

        self.player1 = PlayerHuman(self.board, 'white')
        self.player2 = PlayerHuman(self.board, 'black')

        self.queue = cycle([self.player1, self.player2])
        self.current_player = None
        self.next_round()

    def next_round(self):
        self.current_player = next(self.queue)
        self.current_player.awake()

    def handle_touch(self, field_id):
        self.current_player.handle_touch(field_id)
        if self.current_player.state == 'Done':
            self.next_round()
