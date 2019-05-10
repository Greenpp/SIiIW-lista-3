from board import Board
from piece import Piece

PIECES = 9
JUMP_THRESHOLD = 3

EVENT_NULL = 'n'
EVENT_MILL = 'm'
EVENT_DOUBLE_MILL = '2m'
EVENT_REMOVED = 'rm'
EVENT_SELECTED_MV = 'sm'
EVENT_SELECTED_JMP = 'sj'
EVENT_MOVED = 'mv'


class _Player:
    def __init__(self, board, color, enemy_color, name=None):
        self.name = name if name is not None else f'Player_{color}'
        self.board = board
        self.color = color
        self.enemy_color = enemy_color
        self.placed = 0
        self.state = _StateDone()
        self.selected = None

    def handle_touch(self, field_id):
        pass

    def awake(self):
        if self.placed < PIECES:
            self.state = _StatePlace()
        else:
            self.state = _StateSelect()


class PlayerHuman(_Player):
    def handle_touch(self, field_id):
        event = EVENT_NULL
        if self.state == 'Place':
            possible_moves = self.board.get_empty_fields()
            if field_id in possible_moves:
                self.board.place(field_id, Piece(self.color))
                self.placed += 1
                in_mills = self.board.in_mill(field_id)
                if in_mills == 2:
                    event = EVENT_DOUBLE_MILL
                elif in_mills:
                    event = EVENT_MILL
                else:
                    event = EVENT_SELECTED_MV
        elif self.state == 'Remove':
            possible_moves = self.board.get_color_fields(self.enemy_color)
            if field_id in possible_moves and not self.board.in_mill(field_id):
                self.board.remove(field_id)
                event = EVENT_REMOVED
        elif self.state == 'Select':
            possible_selections = self.board.get_color_fields(self.color)
            if field_id in possible_selections:
                self.selected = field_id
                event = EVENT_SELECTED_MV if len(possible_selections) > JUMP_THRESHOLD else EVENT_SELECTED_JMP
        elif self.state == 'Move':
            possible_selections = self.board.get_color_fields(self.color)
            if field_id in possible_selections:
                self.selected = field_id
                event = EVENT_SELECTED_MV
            else:
                possible_moves = self.board.get_moves(self.selected)
                if field_id in possible_moves:
                    self.board.move(self.selected, field_id)
                    event = EVENT_MILL if self.board.in_mill(field_id) else EVENT_MOVED
        elif self.state == 'Jump':
            possible_selections = self.board.get_color_fields(self.color)
            if field_id in possible_selections:
                self.selected = field_id
                event = EVENT_SELECTED_JMP
            else:
                possible_moves = self.board.get_jumps(self.selected)
                if field_id in possible_moves:
                    self.board.move(self.selected, field_id)
                    event = EVENT_MILL if self.board.in_mill(field_id) else EVENT_MOVED

        self.state = self.state.on_event(event)


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
        if event == EVENT_SELECTED_MV:
            return _StateDone()
        elif event == EVENT_MILL:
            return _StateRemove(1)
        elif event == EVENT_DOUBLE_MILL:
            return _StateRemove(2)
        return self


class _StateSelect(_PlayerState):
    def on_event(self, event):
        if event == EVENT_SELECTED_MV:
            return _StateMove()
        elif event == EVENT_SELECTED_JMP:
            return _StateJump()
        return self


class _StateMove(_PlayerState):
    def on_event(self, event):
        if event == EVENT_MOVED:
            return _StateDone()
        elif event == EVENT_MILL:
            return _StateRemove(1)
        return self


class _StateJump(_PlayerState):
    def on_event(self, event):
        if event == EVENT_MOVED:
            return _StateDone()
        elif event == EVENT_MILL:
            return _StateRemove(1)
        return self


class _StateRemove(_PlayerState):
    def __init__(self, num):
        self.num = num

    def on_event(self, event):
        if event == EVENT_REMOVED:
            self.num -= 1
            if not self.num:
                return _StateDone()
        return self


class _StateDone(_PlayerState):
    def on_event(self, event):
        return self
