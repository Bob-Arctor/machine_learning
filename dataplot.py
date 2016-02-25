# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 12:40:23 2016

@author: AKononov
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class dataplot:
    def __init__(self, plot_type):
        self.plt_type = plot_type
        self.vars = []
        self.types = {'histogram':['x'],
                      'scatterplot':['x','y'], 
                      'hexbin':['x','y'], 
                      'KDE':['x','y'], 
                      'boxplot':['x','y'] }
        
    @staticmethod
    def get_plot_types():
        # return a dict with list of available plots
        # values are lists of needed variables,         
        return {'histogram':['x'],
                'scatterplot':['x','y'],
                'hexbin':['x','y'],
                'KDE':['x','y'],
                'boxplot':['x','y'],
                }
                
    def make_plot(self, variables, df):
        # if all variables are there
        if len(variables) == len(self.types[self.plt_type]):
            # make a plot based on type
            if self.plt_type == 'histogram':
                sns.set_style("whitegrid") 
                self.figure = plt.figure();
                # making plot
                self.figure.clf()
                self.subplot = self.figure.add_subplot(111)
                sns.distplot(df[variables[0]], ax=self.subplot)                
            elif self.plt_type == 'scatterplot':
                jg = sns.jointplot(x=variables[0], y=variables[1], data=df);
                self.figure =jg.fig