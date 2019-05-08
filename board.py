from field import Field
from mill import Mill

NAMES = ['a1', 'd1', 'g1', 'b2', 'd2', 'f2', 'c3', 'd3', 'e3', 'a4', 'b4', 'c4', 'e4', 'f4', 'g4', 'c5', 'd5', 'e5',
         'b6', 'd6', 'f6', 'a7', 'd7', 'g7', ]


class Board:
    def __init__(self):
        fields = [Field(n) for n in NAMES]
        # Horizontal
        for i in range(8):
            mill_fields = [fields[i * 3 + j] for j in range(3)]
            mill = Mill(mill_fields)

            for field in mill_fields:
                field.add_mill(mill)

            mill_fields[1].connect(mill_fields[0])
            mill_fields[1].connect(mill_fields[2])
        # Vertical
        fields.sort(key=lambda x: x.id)
        for i in range(8):
            mill_fields = [fields[i * 3 + j] for j in range(3)]
            mill = Mill(mill_fields)

            for field in mill_fields:
                field.add_mill(mill)

            mill_fields[1].connect(mill_fields[0])
            mill_fields[1].connect(mill_fields[2])

        self.fields = {f.id: f for f in fields}

    def get_empty_fields(self):
        return [id_ for id_, f in self.fields if f.occupation is None]

    def get_color_fields(self, color):
        return [id_ for id_, f in self.fields if f.occupation is not None and f.occupation.color == color]

    def place(self, dest, piece):
        self.fields[dest].occupation = piece

    def move(self, source, dest):
        piece = self.fields[source].occupation
        piece.last_position = source
        self.fields[dest].occupation = piece

        self.fields[source].occupation = None

    def get_state(self):
        pass

    def load_state(self):
        pass
