from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from gui.results_screen import ResultsScreen
from gui.history_screen import HistoryScreen
from gui.upload_screen import UploadScreen  # UploadScreen ayrı dosya olarak gui/upload_screen.py içinde olmalı


class PyClearApp(App):
    def build(self):
        self.title = "PyClear - Python Code Analyzer"
        self.sm = ScreenManager()

        # Screens
        self.upload_screen = UploadScreen(name="upload")
        self.results_screen = ResultsScreen(name="results")
        self.history_screen = HistoryScreen(name="history")

        # Add screens to ScreenManager
        self.sm.add_widget(self.upload_screen)
        self.sm.add_widget(self.results_screen)
        self.sm.add_widget(self.history_screen)

        return self.sm


if __name__ == "__main__":
    PyClearApp().run()
