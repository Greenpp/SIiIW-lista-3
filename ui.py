from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image

from game import Engine


class MorrisApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = Engine()

    def build(self):
        self.title = 'Nine men\'s morris'
        return GameLayout()


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
        self.field_id = id_

    def on_press(self):
        eng = App.get_running_app().engine
        if self.field_id in eng.board.fields:
            img = Image(source='resources\\black_piece.png', pos=self.pos, size=self.size)
            self.add_widget(img)
