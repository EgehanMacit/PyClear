from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from core.db_manager import DBManager

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DBManager()
        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.add_widget(self.layout)
        self.load_history()

    def load_history(self):
        self.layout.clear_widgets()
        scroll = ScrollView(size_hint=(1, 1))
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        history = self.db.get_history()
        if not history:
            grid.add_widget(Label(text="No history available.", size_hint_y=None, height=40))
        else:
            for entry in history:
                file_label = Label(text=f"[b]{entry['file_path']}[/b] ({entry['timestamp']})", markup=True, size_hint_y=None, height=30)
                score = entry['result_data'].get("final_score", 0)
                score_label = Label(text=f"Score: {score}/100", size_hint_y=None, height=30)
                grid.add_widget(file_label)
                grid.add_widget(score_label)
                grid.add_widget(Label(text="—"*50, size_hint_y=None, height=10))

        scroll.add_widget(grid)
        self.layout.add_widget(scroll)

        btn_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=60, spacing=10)
        back_btn = Button(text="Back to Results", on_press=self.go_back)
        btn_layout.add_widget(back_btn)
        self.layout.add_widget(btn_layout)

    def go_back(self, *args):
        self.manager.current = "results"