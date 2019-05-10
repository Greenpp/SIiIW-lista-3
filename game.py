from itertools import cycle
from time import time

from board import Board
from player import PlayerHuman


class Engine:
    def __init__(self):
        self.board = None
        self.player1 = None
        self.player2 = None
        self.round = None
        self.queue = None
        self.current_player = None
        self.round_start_time = None
        self.running = False

    def next_round(self):
        self.round += 1
        if self.round > 18:
            if self.current_won():
                print(f'Player {self.current_player.name} won !')
        self.current_player = next(self.queue)
        print(f'Round {self.round}, player: {self.current_player.name}')
        self.current_player.awake()

    def handle_touch(self, field_id):
        self.current_player.handle_touch(field_id)
        if self.running and self.current_player.state == 'Done':
            self.next_round()

    def get_round_time(self):
        if self.round_start_time is None:
            return 0
        current_time = time()
        delta = current_time - self.round_start_time

        return delta

    def setup(self):
        self.running = False
        self.board = Board()

        color1 = 'white'
        color2 = 'black'

        self.player1 = PlayerHuman(self.board, color1, color2)
        self.player2 = PlayerHuman(self.board, color2, color1)
        self.queue = cycle([self.player1, self.player2])
        self.current_player = self.player1

        self.round_start_time = None
        self.round = 0

    def start(self):
        self.running = True
        self.round_start_time = time()
        self.next_round()

    def current_won(self):
        pieces = self.board.get_color_fields(self.current_player.enemy_color)
        if len(pieces) == 2:
            return True

        return not self.board.has_moves(self.current_player.enemy_color)
