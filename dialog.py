import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog, QTableWidgetItem, QMessageBox
import pandas as pd
import Preproc as prep
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
import random
import seaborn as sns
import dataplot

form_class = uic.loadUiType("main_window.ui")[0]  # Load the UI


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle("proga")
        self.statusBar()
        self.btn_load.clicked.connect(self.btn_load_clicked)  # Bind the event handlers
        self.btn_select_file.clicked.connect(self.selectFile)
        self.btn_set_observ.clicked.connect(self.clicked_observed)
        self.feature_table.cellClicked.connect(self.slotItemClicked)

        self.filepath = ''
        self.dataset = pd.DataFrame()
        self.proc_dataset = pd.DataFrame()  # observed removed
        self.numeric_dataset = pd.DataFrame()  # only numeric features
        self.char_dataset = pd.DataFrame()  # only characteristic features
        self.complete_dataset = pd.DataFrame()
        self.missing_dataset = pd.DataFrame()
        self.observed_dataset = pd.DataFrame()
        self.num_complete_dataset = pd.DataFrame()
        self.num_missing_dataset = pd.DataFrame()
        self.char_complete_dataset = pd.DataFrame()
        self.char_missing_dataset = pd.DataFrame()
        self.observed_index = -1
        #set stats to 0
        self.update_stats()
        #create plots
        # a figure instance to plot on
        self.figure1 = plt.figure()
        self.canvas1 = FigureCanvas(self.figure1)
        self.plot_lay1.addWidget(self.canvas1)
        # button for plotting
        self.btn_plot.clicked.connect(self.plot_features)
        # init of plot combo
        self.fill_plot_combo()
        #connecting combo with function
        self.connect(self.plots_combo, QtCore.SIGNAL('activated(QString)'), self.fill_plot_table)

    def plot_features(self):
        indexes = self.feature_table.selectionModel().selectedRows()
        if len(indexes) == 1 and self.observed_index >=0 :
            item = self.feature_table.item(indexes[0].row(), 1)
            ID = item.text()
            if ID == 'N': # numeric feature
                sns.set_style("whitegrid")                
                # for  numerics we plot histogram and boxplot
                item = self.feature_table.item(indexes[0].row(), 0)
                feat = item.text()
                # making plot
                self.figure1.clf()
                subplot1 = self.figure1.add_subplot(111)
                #self.dataset.plot(kind="scatter", x=feat, y=feat, ax=subplot1)
                #self.dataset.boxplot(column=feat, by = self.observed_name, ax=subplot1)
                sns.boxplot(x=self.observed_name, y=feat, data=self.dataset, ax=subplot1, palette="PRGn")
                sns.stripplot(x=self.observed_name, y=feat, data=self.dataset, jitter=True, edgecolor="gray",ax=subplot1)                
                self.canvas1.draw()

    def clicked_observed(self):
        indexes = self.file_table.selectionModel().selectedColumns()
        if len(indexes) == 1:      
            self.set_observed(indexes[0].column())
            self.lbl_observed.setText(str(self.observed_name))            

    def set_observed(self, index):
        self.observed_dataset = self.dataset[self.dataset.columns[index]].to_frame()
        self.proc_dataset = self.dataset.drop(self.dataset.columns[[index]], axis=1)
        self.observed_index = index
        self.observed_name = self.dataset.columns[index] 
        self.observed_type = prep.series_type(self.observed_dataset.iloc[:,0])
        self.split_dataset()
        self.update_stats()

    def split_dataset(self):
        # generating subsets
        self.complete_dataset, self.missing_dataset = prep.split_complete_data(self.proc_dataset)
        self.numeric_dataset, self.char_dataset = prep.split_features_by_type(self.proc_dataset)
        # self.num_complete_dataset, self.num_missing_dataset = prep.split_complete_data(self.numeric_dataset)
        # self.char_complete_dataset, self.char_missing_dataset = prep.split_complete_data(self.char_dataset)

    def update_stats(self):
        if self.dataset.empty:
            self.stats_table.setColumnCount(0)  # rows and columns of table
            self.stats_table.setRowCount(0)
            self.stats_table.setHorizontalHeaderLabels(['Statistics'])
        else:
            # self.lbl_num_complete.setText(str(self.num_complete_dataset.shape[0]))
            # self.lbl_num_missing.setText(str(self.num_missing_dataset.shape[0]))
            # self.lbl_char_complete.setText(str(self.char_complete_dataset.shape[0]))
            # self.lbl_char_missing.setText(str(self.char_missing_dataset.shape[0]))
            self.stats_table.setColumnCount(2)  # rows and columns of table
            self.stats_table.setRowCount(7)
            # total samples
            self.add_to_table(self.stats_table, 0, ['Total samples', str(self.proc_dataset.shape[0])])
            #total features
            self.add_to_table(self.stats_table, 1, ['Total features', str(self.proc_dataset.shape[1])])
            # complete samples            
            self.add_to_table(self.stats_table, 2, ['Complete samples', str(self.complete_dataset.shape[0])])
            # missing samples            
            self.add_to_table(self.stats_table, 3, ['Missing samples', str(self.missing_dataset.shape[0])])
            # character features            
            self.add_to_table(self.stats_table, 4, ['Character features', str(self.char_dataset.shape[1])])
            # numeric features            
            self.add_to_table(self.stats_table, 5, ['Numeric features', str(self.numeric_dataset.shape[1])])
            # insert subheader
            item = QTableWidgetItem('Observation:')
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.stats_table.setItem(6, 0, item)
            self.stats_table.item(6, 0).setBackground(QtGui.QColor(192,192,192))
            # if observed has been set fill its stats
            if self.observed_index >= 0 :
                rowPosition = self.stats_table.rowCount()
                # type
                if self.observed_type == 'Number':
                    for i in range(5):
                        self.stats_table.insertRow(rowPosition + i)
                    # fill in numeric stats
                    self.add_to_table(self.stats_table, rowPosition, ['Type', self.observed_type])
                    self.add_to_table(self.stats_table, rowPosition + 1, ['Max', self.observed_dataset.meax()])
                    self.add_to_table(self.stats_table, rowPosition + 2, ['Min', self.observed_dataset.min()])
                    self.add_to_table(self.stats_table, rowPosition + 3, ['Mean', self.observed_dataset.mean()])
                    self.add_to_table(self.stats_table, rowPosition + 4, ['Std', self.observed_dataset.std()])
                else:
                    for i in range(2):
                        self.stats_table.insertRow(rowPosition + i)
                    # fill in character stats
                    self.add_to_table(self.stats_table, rowPosition, ['Type', self.observed_type])
                    classes = len(self.observed_dataset.iloc[:,0].unique())
                    self.add_to_table(self.stats_table, rowPosition + 1, ['Unique classes', classes])
            self.fill_feature_table()
                 
    def add_to_table(self, table, row, row_list, set_enabled=True, color=[255,255,255]):
        for col in range(len(row_list)):
            item = QTableWidgetItem(str(row_list[col]))
            if set_enabled :
                item.setFlags(QtCore.Qt.ItemIsEnabled)
            table.setItem(row, col, item)
            table.item(row, col).setBackground(QtGui.QColor(color[0],color[1],color[2]))

    def btn_load_clicked(self):  # read csv file
        self.createProgressBar()
        self.progressBar.setValue(3)
        self.dataset = pd.read_csv(self.lineEdit_filepath.text())
        self.proc_dataset = self.dataset
        self.filepath = self.lineEdit_filepath.text()
        self.progressBar.setValue(25)
        # updating stats
        self.split_dataset()
        self.update_stats()
        # filling table
        self.progressBar.setValue(50)
        self.fill_data_table()

    def selectFile(self):  # open file selection
        self.lineEdit_filepath.setText(QFileDialog.getOpenFileName())

    def createProgressBar(self):
        """
        Create the progress bar.
        """
        self.progressBar = QtGui.QProgressBar(self)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.show()

    def fill_data_table(self):
        if not self.dataset.empty:
            self.file_table.setColumnCount(self.dataset.shape[1])  # rows and columns of table
            self.file_table.setRowCount(self.spin_head.value())
            total = self.dataset.shape[1] + self.spin_head.value()
            counter = 50
            for row in range(self.spin_head.value()):  # add items from array to QTableWidget
                for column in range(self.dataset.shape[1]):
                    item = QTableWidgetItem(
                        str(self.dataset[self.dataset.columns[column]][row]))  # each item is a QTableWidgetItem
                    self.file_table.setItem(row, column, item)
                    counter += 1
                    self.progressBar.setValue(int(counter // total))
            # making cells read-only
            self.file_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            # setting header labels
            self.file_table.setHorizontalHeaderLabels(list(self.dataset.columns))
            # update colorcodes
            self.repaint_table()
            # hide progress bar
            self.progressBar.hide()

    def repaint_table(self, old_ind=-1):
        self.file_table.setAlternatingRowColors(True)
        self.file_table.setStyleSheet("alternate-background-color: lightGray;background-color: white;")

    def fill_feature_table(self):
        if not self.proc_dataset.empty:
            # making a table of features
            self.feature_table.setColumnCount(2)  # rows and columns of table
            self.feature_table.setRowCount(self.dataset.shape[1])
            # if got observed add first
            obs = 0
            if self.observed_index >= 0:
                obs = 1
                row_list = [self.observed_name, str(self.observed_type) + ' [Obs]']
                self.add_to_table(self.feature_table, 0, row_list, False, [255,255,0])
            # adding all other features
            for row in range(self.proc_dataset.shape[1]):
                row_list = [str(self.proc_dataset.columns[row]), prep.series_type(self.proc_dataset[self.proc_dataset.columns[row]])[0:1]]                
                self.add_to_table(self.feature_table, row+obs, row_list, False)                
            # making cells read-only
            self.feature_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            #making it only possible to select rows
            self.feature_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            # setting header labels
            self.feature_table.setHorizontalHeaderLabels(['Features','Type'])
            # update colorcodes
            # self.repaint_feature_table()

    def repaint_feature_table(self):
        self.feature_table.setAlternatingRowColors(True)
        self.feature_table.setStyleSheet("alternate-background-color: lightGray;background-color: white;")
    
    #table with variables to plot, called when combo is changed    
    def fill_plot_table(self, selected_plot):
        # based on the plot type fill the table
        rows = len(self.plot_types[selected_plot])
        self.plot_table.setRowCount(rows)    
        self.plot_table.setColumnCount(2)
        #adding buttons
        for index in range(rows):
            self.btn_sell = QtGui.QPushButton(self.plot_types[selected_plot][index] + '=>')
            self.btn_sell.clicked.connect(self.table_btn_clicked)
            self.plot_table.setCellWidget(index,0,self.btn_sell)
        self.plot_table.setHorizontalHeaderLabels(['','Variable'])
    
    # initialization ofplot combo        
    def fill_plot_combo(self):
        # filling combobox
        self.plot_types = dataplot.dataplot.get_plot_types()
        for key in self.plot_types.keys():
            self.plots_combo.addItem(str(key))
        #init of plot vars table
        self.fill_plot_table(self.plots_combo.currentText())
        
    def table_btn_clicked(self):
        button = QtGui.qApp.focusWidget()
        # or button = self.sender()
        index = self.plot_table.indexAt(button.pos())
        if index.isValid():
           # print(index.row(), index.column()) 
            #drop in selected item
            indexes = self.feature_table.selectionModel().selectedRows()
            print(indexes[0].row())
            if len(indexes) == 1 :
                item0 = self.feature_table.item(indexes[0].row(), 0)
                item1 = self.feature_table.item(indexes[0].row(), 1)
                feat = item0.text()
                feat_type = item1.text()
                item0 = QTableWidgetItem(feat)
                item0.setFlags(QtCore.Qt.ItemIsEnabled)
                item1 = QTableWidgetItem(feat_type)
                item1.setFlags(QtCore.Qt.ItemIsEnabled)                
                self.plot_table.setItem(index.row(), 1, item0)
                self.plot_table.setItem(index.row(), 2, item1)
                
    def slotItemClicked(self, row, col):
        item = self.feature_table.item(row, 0)
        feature = item.text()
        self.feature_stats_table.setColumnCount(2)
        self.feature_stats_table.setRowCount(0)
        self.feature_stats_table.setHorizontalHeaderLabels([feature,'stats'])
        self.fill_feature_stats_table(self.feature_stats_table, self.dataset[feature], 0)
        #QMessageBox.information(self,"QTableWidget Cell Click","Row: " + str(row) + " |Column: " + str(col) + " text: " + ID)
        return
        
    def fill_feature_stats_table(self, table, df_col, rowPosition):
        # type
        col_type = prep.series_type(df_col)
        if col_type == 'Number':
            for i in range(5):
                table.insertRow(rowPosition + i)
            # fill in numeric stats
            self.add_to_table(table, rowPosition, ['Type', col_type])
            self.add_to_table(table, rowPosition + 1, ['Max', df_col.max()])
            self.add_to_table(table, rowPosition + 2, ['Min', df_col.min()])
            self.add_to_table(table, rowPosition + 3, ['Mean', df_col.mean()])
            self.add_to_table(table, rowPosition + 4, ['Std', df_col.std()])
        else:
            for i in range(2):
                table.insertRow(rowPosition + i)
            # fill in character stats
            self.add_to_table(table, rowPosition, ['Type', col_type])
            classes = len(df_col.unique())
            self.add_to_table(table, rowPosition + 1, ['Unique classes', classes])



app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
