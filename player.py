from board import Board
from piece import Piece

PIECES = 2

EVENT_EMPTY_FIELD = 'empty_field'
EVENT_MILL = 'mill'


class _Player:
    def __init__(self, board, color, name=None):
        self.name = name if name is not None else f'Player_{color}'
        self.board = board
        self.color = color
        self.placed = 0  # placed pieces
        self.state = _StatePlace()

    def handle_touch(self, field_id):
        pass

    def awake(self):
        if self.placed < PIECES:
            self.state = _StatePlace()
        else:
            self.state = _StateSelect()


class PlayerHuman(_Player):
    def handle_touch(self, field_id):
        if self.state == 'Place':
            possible_moves = self.board.get_empty_fields()
            if field_id in possible_moves:
                self.board.place(field_id, Piece(self.color))
                self.placed += 1
                self.state = self.state.on_event(EVENT_EMPTY_FIELD)


class PlayerAI(_Player):
    def __init__(self, board, color, name=None):
        super().__init__(board, color, name)
        self.simulation = Board()


class _PlayerState:
    def on_event(self, event):
        pass

    def __eq__(self, other):
        return self.__class__.__name__.endswith(other)


class _StatePlace(_PlayerState):
    def on_event(self, event):
        if event == EVENT_EMPTY_FIELD:
            return _StateDone()
        elif event == EVENT_MILL:
            return _StateRemove()
        return self


class _StateSelect(_PlayerState):
    pass


class _StateMove(_PlayerState):
    pass


class _StateRemove(_PlayerState):
    pass


class _StateDone(_PlayerState):
    pass
