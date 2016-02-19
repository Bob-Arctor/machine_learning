from kivy.uix.tabbedpanel import TabbedPanel
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import *
import pandas as pd
import os
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
import Preproc


class RootWidget(FloatLayout):
    #data
    samples_df = ObjectProperty(pd.DataFrame(), force_dispatch=True)
    samples_full_df = ObjectProperty(pd.DataFrame(), force_dispatch=True)
    samples_missing_df = ObjectProperty(pd.DataFrame(), force_dispatch=True)
    results_df = ObjectProperty(pd.DataFrame(), force_dispatch=True)
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
            self.samples_df = pd.read_csv(self.samples_data_file)
            self.update_samples_stats()
            self.update_analysis()
        except IndexError:
            popup = Popup(title='File loading error', 
                          content=Label(text='Please select .csv file with sample points'),
                          size_hint=(None, None), size=(400, 400))
            popup.open()

    def load_results(self, path, filename):
        self.results_data_file = os.path.join(path, filename[0])
        self.results = pd.read_csv(self.samples_data_file)

    def update_samples_stats(self):
        self.total_samples = str(self.samples_df.shape[0])
        self.total_features = str(self.samples_df.shape[1])
        self.samples_full_df, self.samples_missing_df = Preproc.split_complete_data(self.samples_df)
        self.samples_with_missing = str(self.samples_missing_df.shape[0])
        self.numerical_features = str(Preproc.get_total_numeric_features(self.samples_df))
        self.categorical_features = str(Preproc.get_total_categorical_features(self.samples_df))
        
    def update_analysis(self):
        features_list = self.ids.features_list
        for i in range(30):
            features_list.add_widget(ScrollButton(text=str(i), group='feature'))

class ScrollButton(ToggleButton):
    pass

class MainApp(App):
    def build(self):
        root = RootWidget()
        return root


if __name__ == '__main__':
    MainApp().run()
