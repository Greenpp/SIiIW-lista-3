from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock

from game import Engine


class MorrisApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.engine = Engine()
        self.engine.setup()
        self.fields = []

    def build(self):
        self.title = 'Nine men\'s morris'
        return GameLayout()

    def update_board_view(self):
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

    def on_start(self):
        self.update_players()

    def update_players(self):
        p1 = self.engine.player1
        p2 = self.engine.player2
        name1 = p1.name
        name2 = p2.name

        if p2.state == 'Done':
            name1 = f'[b]{name1}[/b]'
        else:
            name2 = f'[b]{name2}[/b]'

        label1 = self.root.ids.player1_label
        label2 = self.root.ids.player2_label

        label1.text = name1
        label2.text = name2

    def update_clock(self, dt):
        round_time = self.engine.get_round_time()
        round_sec = round(round_time)
        mins = round_sec // 60
        secs = round_sec % 60

        label = self.root.ids.clock_label
        label.text = f'{mins:02}:{secs:02}'

    def start_game(self):
        self.root.ids.start_button.disabled = True
        self.engine.start()
        self.update_players()
        self.root.ids.reset_button.disabled = False

    def reset_game(self):
        self.root.ids.reset_button.disabled = True
        self.engine.setup()
        self.update_clock(None)
        self.update_board_view()
        self.update_players()
        self.root.ids.start_button.disabled = False


class GameLayout(GridLayout):
    pass


class ClockLabel(Label):
    def __init__(self, **kwargs):
        super(ClockLabel, self).__init__(**kwargs)
        callback = App.get_running_app().update_clock
        Clock.schedule_interval(callback, 1)


class BoardLayout(GridLayout):
    def __init__(self, **kwargs):
        super(BoardLayout, self).__init__(**kwargs)
        for n in reversed('abcdefg'):
            for i in range(7):
                button = FieldButton(f'{n}{i + 1}')
                self.add_widget(button)


class StartButton(Button):
    def __init__(self, **kwargs):
        super(StartButton, self).__init__(**kwargs)

    def on_press(self):
        app = App.get_running_app()
        app.start_game()


class ResetButton(Button):
    def __init__(self, **kwargs):
        super(ResetButton, self).__init__(**kwargs)

    def on_press(self):
        app = App.get_running_app()
        app.reset_game()


class FieldButton(Button):
    def __init__(self, id_, **kwargs):
        super(FieldButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.border = (0, 0, 0, 0)
        self.field_id = id_

    def on_press(self):
        app = App.get_running_app()
        eng = app.engine

        eng.handle_touch(self.field_id)
        app.update_board_view()
        app.update_players()

    def clear(self):
        self.background_color = (0, 0, 0, 0)

    def set_black(self):
        self.background_color = (1, 1, 1, 1)
        self.background_normal = 'resources/black_piece.png'
        self.background_down = 'resources/black_piece.png'

    def set_white(self):
        self.background_color = (1, 1, 1, 1)
        self.background_normal = 'resources/white_piece.png'
        self.background_down = 'resources/white_piece.png'

    def set_possible_move(self):
        pass

    def set_possible_remove(self):
        pass
