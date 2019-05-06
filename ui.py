from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from game import Engine


class MorrisApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = Engine()
        self.fields = []

    def build(self):
        self.title = 'Nine men\'s morris'
        return GameLayout()

    def update_board_view(self):
        if not self.fields:
            fields = self.root.ids.board_view.children
            self.fields = [(f, self.engine.board.fields[f.field_id]) for f in fields if
                           f.field_id in self.engine.board.fields]
        for widget, field in self.fields:
            if field.occupation is None:
                widget.clear()
            elif field.occupation.color == 'white':
                widget.set_white()
            else:
                widget.set_black()


class GameLayout(GridLayout):
    pass


class BoardLayout(GridLayout):
    def __init__(self, **kwargs):
        super(BoardLayout, self).__init__(**kwargs)
        for n in reversed('abcdefg'):
            for i in range(7):
                button = FieldButton(f'{n}{i + 1}')
                self.add_widget(button)


class FieldButton(Button):
    def __init__(self, id_, **kwargs):
        super(FieldButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.border = (0, 0, 0, 0)
        self.field_id = id_

    def on_press(self):
        app = App.get_running_app()
        eng = app.engine
        if eng.handle_touch(self.field_id):
            app.update_board_view()

    def clear(self):
        self.background_color = (0, 0, 0, 0)

    def set_black(self):
        self.background_color = (1, 1, 1, 1)
        self.background_normal = 'resources\\black_piece.png'
        self.background_down = 'resources\\black_piece.png'

    def set_white(self):
        self.background_color = (1, 1, 1, 1)
        self.background_normal = 'resources\\white_piece.png'
        self.background_down = 'resources\\white_piece.png'
