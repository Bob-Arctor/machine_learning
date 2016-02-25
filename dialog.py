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

    def plot_features(self):
        data = [random.random() for i in range(10)]
        # ax = self.figure.add_subplot(111)
        # discards the old graph
        # ax.hold(False)
        # plot data
        # ax.plot(data, 'o-')
        # refresh canvas
        # self.canvas.draw()
        indexes = self.feature_table.selectionModel().selectedRows()
        if len(indexes) == 1 and self.observed_index >=0 :
            item = self.feature_table.item(indexes[0].row(), 1)
            ID = item.text()
            if ID == 'N': # numeric feature
                # for  numerics we plot histogram and boxplot
                item = self.feature_table.item(indexes[0].row(), 0)
                feat = item.text()
                print(feat)
                # making plot
                self.figure1.clf()
                subplot1 = self.figure1.add_subplot(111)
                #self.dataset.plot(kind="scatter", x=feat, y=feat, ax=subplot1)
                #self.dataset.boxplot(column=feat, by = self.observed_name, ax=subplot1)
                sns.boxplot(x=self.observed_name, y=feat, data=self.dataset, ax=subplot1, palette="PRGn")
                sns.stripplot(x=self.observed_name, y=feat, data=self.dataset, jitter=True, edgecolor="gray",ax=subplot1)                
                #subplot1.set(ylim=(self.dataset[feat].min(), self.dataset[feat].max()))                
                #self.mw_1.draw()
                #self.figure1.tight_layout()
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
        
    def slotItemClicked(self, row, col):
        #item = self.feature_table.item(row, col)
        #ID = item.text()
        
        #QMessageBox.information(self,"QTableWidget Cell Click","Row: " + str(row) + " |Column: " + str(col) + " text: " + ID)
        return


app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
