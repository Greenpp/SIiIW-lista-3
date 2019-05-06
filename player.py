from piece import Piece


class Player:
    def __init__(self, name, board, color):
        self.name = name
        self.board = board
        self.pieces = [Piece(color) for i in range(9)]

    def handle_touch(self, field_id):
        if self.pieces:
            # Placing phase
            piece = self.pieces.pop()
            if not self.board.place(field_id, piece):
                self.pieces.append(piece)
