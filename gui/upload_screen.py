import os
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView
from kivy.app import App
from kivy.properties import StringProperty
from core.analyzer import CodeAnalyzer

class UploadScreen(Screen):
    selected_file_path = StringProperty("")
    file_content = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        self.title_label = Label(text="[b]     PyClear \nDosya Seçin[/b]",
                                 markup=True, font_size='24sp', size_hint_y=None, height=60)
        layout.add_widget(self.title_label)

        self.path_label = Label(text="Seçilen Dosya: Yok", size_hint_y=None, height=30)
        layout.add_widget(self.path_label)

        # FileChooser
        self.file_chooser = FileChooserIconView(path=".", filters=["*.py"])
        layout.add_widget(self.file_chooser)

        self.analyze_button = Button(text="Analizi Başlat", size_hint_y=None, height=60,
                                     on_press=self.start_analysis)
        layout.add_widget(self.analyze_button)

        self.add_widget(layout)

    def start_analysis(self, instance):
        selection = self.file_chooser.selection
        if not selection:
            self.path_label.text = "⚠ Lütfen bir dosya seçin!"
            return

        self.selected_file_path = selection[0]
        self.path_label.text = f"Seçilen Dosya: {os.path.basename(self.selected_file_path)}"

        try:
            with open(self.selected_file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.file_content = f.read()

            # file_path parametresi kaldırıldı
            analyzer = CodeAnalyzer(code_text=self.file_content)
            results = analyzer.analyze()

            # Dosya yolunu elle ekleyebilirsin
            results["file_path"] = self.selected_file_path

            # ScreenManager üzerinden ResultsScreen'e geçiş
            app = App.get_running_app()
            result_screen = app.sm.get_screen("results")
            result_screen.show_results(results)
            app.sm.current = "results"

        except Exception as e:
            self.path_label.text = f"Analiz hatası: {e}"
            print(f"ERROR DURING ANALYSIS: {e}")

        except Exception as e:
            self.path_label.text = f"Analiz hatası: {e}"
            print(f"ERROR DURING ANALYSIS: {e}")
