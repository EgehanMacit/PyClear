from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.utils import get_color_from_hex
from utils.pdf_report import create_pdf_report
from core.db_manager import DBManager

class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_data = None
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)
        self.db = DBManager()  # DB instance

    def show_results(self, result_data):
        self.layout.clear_widgets()
        self.result_data = result_data

        file_path = result_data.get("file_path", "Unknown File")

        # Save record
        try:
            self.db.add_record(file_path, result_data)
        except Exception as e:
            print(f"[DB Error] {e}")

        # Title
        title = Label(
            text=f"[b]PyClear Analysis Results[/b]\n[i]{file_path}[/i]",
            font_size=22,
            markup=True,
            size_hint_y=None,
            height=80
        )
        self.layout.add_widget(title)

        scroll = ScrollView(size_hint=(1, 1))
        inner = GridLayout(cols=1, spacing=10, size_hint_y=None)
        inner.bind(minimum_height=inner.setter('height'))

        # Suggestions
        inner.add_widget(Label(text="[b]Suggestions / Recommendations[/b]", markup=True, font_size=20, size_hint_y=None, height=40))
        for s in result_data.get("suggestions", []):
            inner.add_widget(Label(text=f"• {s}", halign="left", size_hint_y=None, height=30))

        # PEP8
        inner.add_widget(Label(text="[b]PEP8 Issues[/b]", markup=True, font_size=20, size_hint_y=None, height=40))
        for issue in result_data.get("pep8_issues", []):
            inner.add_widget(Label(text=f"• {issue}", halign="left", size_hint_y=None, height=30))

        # Security
        inner.add_widget(Label(text="[b]Security Warnings[/b]", markup=True, font_size=20, size_hint_y=None, height=40))
        for s in result_data.get("security_issues", []):
            inner.add_widget(Label(text=f"• {s}", halign="left", size_hint_y=None, height=30))

        # Metrics
        inner.add_widget(Label(text="[b]Code Metrics[/b]", markup=True, font_size=20, size_hint_y=None, height=40))
        for k, v in result_data.get("metrics", {}).items():
            inner.add_widget(Label(text=f"{k}: {v}", size_hint_y=None, height=30))

        # Final score
        score = result_data.get('final_score', 0)
        color = self.get_score_color(score)
        score_label = Label(text=f"[b]Final Score: {score}/100[/b]", font_size=24, markup=True,
                            color=get_color_from_hex(color), size_hint_y=None, height=60)
        inner.add_widget(score_label)

        scroll.add_widget(inner)
        self.layout.add_widget(scroll)

        # Buttons
        btn_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=60, spacing=10)
        pdf_btn = Button(text="Export as PDF", on_press=self.export_pdf)
        back_btn = Button(text="Back to Upload", on_press=self.go_back)
        history_btn = Button(text="View History", on_press=self.view_history)
        btn_layout.add_widget(pdf_btn)
        btn_layout.add_widget(back_btn)
        btn_layout.add_widget(history_btn)
        self.layout.add_widget(btn_layout)

        self.show_popup("Analysis Complete", f"File analyzed successfully:\n{file_path}")

    def export_pdf(self, *args):
        if not self.result_data:
            return
        create_pdf_report(self.result_data)
        self.show_popup("PDF Created", "Report successfully saved in the /reports directory.")

    def go_back(self, *args):
        self.manager.current = "upload"

    def view_history(self, *args):
        try:
            app = App.get_running_app()
            history_screen = app.sm.get_screen("history")
            history_screen.load_history()
            app.sm.current = "history"
        except Exception as e:
            self.show_popup("History Error", str(e))

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_btn = Button(text="Close", size_hint_y=None, height=40)
        content.add_widget(close_btn)
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def get_score_color(self, score):
        if score >= 80:
            return "#00FF00"
        elif score >= 50:
            return "#FFD700"
        else:
            return "#FF4500"
