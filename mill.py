class Mill:
    def __init__(self, fields):
        self.fields = fields

    def check(self):
        color = None
        for field in self.fields:
            if field.occupation is None:
                return False
            elif color is None:
                color = field.occupation.color
            elif color != field.occupation.color:
                return False
        return True
