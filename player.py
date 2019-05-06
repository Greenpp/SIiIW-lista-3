from piece import Piece

PIECES = 2


class Player:
    def __init__(self, name, board, color):
        self.name = name
        self.board = board
        self.color = color
        self.pieces = [Piece(color) for i in range(PIECES)]
        self.selected = None

    def handle_touch(self, field_id):
        if self.pieces:
            # Placing phase
            piece = self.pieces.pop()
            if not self.board.place(field_id, piece):
                self.pieces.append(piece)
                return False
            return True
        else:
            field = self.board.fields[field_id]
            if field.occupation is not None:
                if self.is_my_piece(field.occupation):
                    self.selected = field
            elif self.selected is not None and self.selected.is_neighbour(field):
                self.board.move(self.selected.id, field_id)
                self.selected = None
                return True
            return False

    def is_my_piece(self, piece):
        return piece.color == self.color
