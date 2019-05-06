class Field:
    def __init__(self, id_):
        self.occupation = None
        self.neighbours = []
        self.mills = []

        self.id = id_

    def __hash__(self):
        return hash(self.id)

    def add_mill(self, mill):
        self.mills.append(mill)

    def connect(self, nbr):
        self.neighbours.append(nbr)
        nbr.neighbours.append(self)

    def is_neighbour(self, field):
        return field in self.neighbours
