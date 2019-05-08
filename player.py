from board import Board
from piece import Piece

PIECES = 3

EVENT_EMPTY_FIELD = 'empty_field'
EVENT_MILL = 'mill'
EVENT_REMOVED = 'removed'


class _Player:
    def __init__(self, board, color, enemy_color, name=None):
        self.name = name if name is not None else f'Player_{color}'
        self.board = board
        self.color = color
        self.enemy_color = enemy_color
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
                event = EVENT_MILL if self.board.in_mill(field_id) else EVENT_EMPTY_FIELD
                self.state = self.state.on_event(event)
        elif self.state == 'Remove':
            possible_moves = self.board.get_color_fields(self.enemy_color)
            if field_id in possible_moves:
                self.board.remove(field_id)
                self.state = self.state.on_event(EVENT_REMOVED)


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
    def on_event(self, event):
        if event == EVENT_REMOVED:
            return _StateDone()
        return self


class _StateDone(_PlayerState):
    pass
