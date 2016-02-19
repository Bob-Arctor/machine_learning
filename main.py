from kivy.uix.tabbedpanel import TabbedPanel
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
import pandas as pd
import os
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import Preproc


class RootWidget(FloatLayout):
    #data
    samples = ObjectProperty(pd.DataFrame(), force_dispatch=True)
    results = ObjectProperty(pd.DataFrame(), force_dispatch=True)
    #stats label text fields
    samples_data_file = StringProperty('')
    results_data_file = StringProperty('')
    total_samples = StringProperty('')
    total_features = StringProperty('')
    samples_with_missing = StringProperty('')
    numerical_features = StringProperty('')
    categorical_features = StringProperty('')

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
        self.total_samples = str(self.samples.shape[0])
        self.total_features = str(self.samples.shape[1])
        self.numerical_features = str(Preproc.get_total_numeric_features(self.samples))
        self.categorical_features = str(Preproc.get_total_categorical_features(self.samples))

class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == '__main__':
    MainApp().run()
