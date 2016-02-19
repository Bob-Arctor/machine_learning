from kivy.uix.tabbedpanel import TabbedPanel
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
import pandas as pd
import os
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class RootWidget(FloatLayout):
    samples = ObjectProperty(pd.DataFrame(), force_dispatch=True)
    results = ObjectProperty(pd.DataFrame(), force_dispatch=True)
    samples_data_file = StringProperty('')
    results_data_file = StringProperty('')
    total_samples = StringProperty('')
    total_features = StringProperty('')

    def load_samples(self, path, filename):
        try:
            self.samples_data_file = os.path.join(path, filename[0])
            self.samples = pd.read_csv(self.samples_data_file)
            self.update_samples_stats()
        except IndexError:
            popup = Popup(title='File loading error', content=Label(text='Please select .csv file with sample points'),
                          size_hint=(None, None), size=(400, 400))
            popup.open()

    def load_results(self, path, filename):
        self.results_data_file = os.path.join(path, filename[0])
        self.results = pd.read_csv(self.samples_data_file)

    def update_samples_stats(self):
        print(self.samples.shape[0])
        print(self.samples.shape[1])
        self.total_samples = str(self.samples.shape[0])
        self.total_features = str(self.samples.shape[1])
        print(self.total_features)


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
