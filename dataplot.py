# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 12:40:23 2016

@author: AKononov
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class dataplot:
    def __init__(self):
        self.plt_type = ''
        self.vars = []
        # limit of discrete classes for plotting
        self.discr_limit = 20
        self.types = {'histogram': ['x'],
                      'scatterplot': ['x', 'y'],
                      'hexbin': ['x', 'y'],
                      'KDE': ['x', 'y'],
                      'boxplot': ['x', 'y'],
                      'robust lin regression': ['x', 'y'],
                      '2nd order regression': ['x', 'y'],
                      'discrete lin regression': ['x', 'y'],
                      'Y-binary regression': ['x', 'y'],
                      'Lowess smoother': ['x', 'y'],
                      'category regression': ['x', 'y', 'z'],
                      'Violin plot':['x','y'],
                      'discrete histogram':['x'],
                      'pairgrid':['x','y','z']}

    def get_plot_types(self):
        # return a dict with list of available plots
        # values are lists of needed variables,
        return self.types

    def set_plot_type(self, plot_type):
        pass

    def make_plot(self, variables, df):
        # if all variables are there
        if len(variables) == len(self.types[self.plt_type]):
            # make a plot based on type
            sns.set(style="whitegrid", color_codes=True)
            if self.plt_type == 'histogram':
                self.figure = plt.figure()
                # making plot
                self.figure.clf()
                self.subplot = self.figure.add_subplot(111)
                sns.distplot(df[variables[0]], ax=self.subplot)
            elif self.plt_type == 'scatterplot':
                jg = sns.jointplot(x=variables[0], y=variables[1], data=df, kind="reg")
                self.figure = jg.fig
            elif self.plt_type == 'boxplot':
                # raise exception if too many classes - possible datatype error                
                if len(df[variables[0]].unique()) > self.discr_limit:
                    raise TypeError('Too many classes. Type error?')
                self.figure = plt.figure()
                # making plot
                self.figure.clf()
                self.subplot = self.figure.add_subplot(111)
                sns.boxplot(x=variables[0], y=variables[1], data=df, ax=self.subplot, palette="PRGn")
                sns.stripplot(x=variables[0], y=variables[1], data=df, jitter=True, edgecolor="gray", ax=self.subplot)
            elif self.plt_type == 'KDE':
                jg = sns.jointplot(x=variables[0], y=variables[1], data=df, kind="kde")
                self.figure = jg.fig
            elif self.plt_type == 'hexbin':
                with sns.axes_style("white"):
                    jg = sns.jointplot(x=df[variables[0]], y=df[variables[1]], kind="hex", color="k")
                    self.figure = jg.fig
            elif self.plt_type == 'robust lin regression':
                jg = sns.lmplot(x=variables[0], y=variables[1], data=df, robust=True, ci=None, scatter_kws={"s": 80})
                self.figure = jg.fig
            elif self.plt_type == '2nd order regression':
                jg = sns.lmplot(x=variables[0], y=variables[1], data=df, order=2, ci=None, scatter_kws={"s": 80})
                self.figure = jg.fig
            elif self.plt_type == 'discrete lin regression':
                jg = sns.lmplot(x=variables[0], y=variables[1], data=df, x_estimator=np.mean)
                self.figure = jg.fig
            elif self.plt_type == 'Y-binary regression':
                jg = sns.lmplot(x=variables[0], y=variables[1], data=df, logistic=True, y_jitter=.03)
                self.figure = jg.fig
            elif self.plt_type == 'Lowess smoother':
                jg = sns.lmplot(x=variables[0], y=variables[1], data=df, lowess=True)
                self.figure = jg.fig
            elif self.plt_type == 'category regression':
                jg = sns.lmplot(x=variables[0], y=variables[1], hue=variables[2], data=df)
                self.figure = jg.fig
            elif self.plt_type == 'Violin plot':
                self.figure = plt.figure()
                # making plot
                self.figure.clf()
                self.subplot = self.figure.add_subplot(111)
                sns.violinplot(x=variables[0], y=variables[1], data=df, inner=None, ax=self.subplot)
                sns.swarmplot(x=variables[0], y=variables[1], data=df, color="w", alpha=.5, ax=self.subplot)
            elif self.plt_type == 'discrete histogram':
                self.figure = plt.figure()
                # making plot
                self.figure.clf()
                self.subplot = self.figure.add_subplot(111)
                sns.countplot(x=variables[0], data=df, palette="PRGn", ax=self.subplot)
            elif self.plt_type == 'pairgrid':
                jg = sns.PairGrid(df, vars=[variables[0], variables[1]], hue=variables[2])
                jg.map_upper(plt.scatter)
                jg.map_lower(sns.kdeplot)
                jg.map_diag(plt.hist)
                self.figure = jg.fig

