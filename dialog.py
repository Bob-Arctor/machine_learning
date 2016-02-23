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
        self.setWindowTitle("прога")
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
        # self.figure = plt.figure()
        # self.canvas = FigureCanvas(self.figure)
        self.btn_plot.clicked.connect(self.plot_features)
        # self.plot_layout.addWidget(self.canvas)

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
        print(indexes)
        print(len(indexes))
        print(self.observed_index)
        print(indexes[0].row())
        if len(indexes) == 1 and self.observed_index >=0 :
            item = self.feature_table.item(indexes[0].row(), 1)
            ID = item.text()
            print(ID)
            if ID == 'N': # numeric feature
                # for  numerics we plot histogram and boxplot
                item = self.feature_table.item(indexes[0].row(), 0)
                feat = item.text()
                print(feat)
                subplot1 = self.mw_1.figure.add_subplot(111)
                self.dataset.plot(kind="scatter", x=feat, y=feat, ax=subplot1)
                #self.dataset.boxplot(column=feat, by = self.observed_name, ax=subplot1)
                # sns.boxplot(x=self.observed_name, y=feat, data=self.dataset, ax=subplot1, palette="PRGn")
                # sns.stripplot(x=self.observed_name, y=feat, data=self.dataset, jitter=True, edgecolor="gray",ax=subplot1)                
                # subplot1.set(ylim=(self.dataset[feat].min(), self.dataset[feat].max()))                
                self.mw_1.draw()

    def clicked_observed(self):
        indexes = self.file_table.selectionModel().selectedColumns()
        if len(indexes) == 1:
            old_ind = self.observed_index       
            self.observed_index = indexes[0].column()
            self.observed_name = self.dataset.columns[self.observed_index]
            self.set_observed(self.observed_index)            
            self.split_dataset()
            self.update_stats()
            self.repaint_table(old_ind)
            # for index in sorted(indexes):
            #    print('column %d is selected' % index.column())

    def set_observed(self, index):
        self.proc_dataset = self.dataset.drop(self.dataset.columns[[index]], axis=1)
        self.observed_dataset = self.dataset[self.dataset.columns[index]].to_frame()

    def split_dataset(self):
        # generating subsets
        self.complete_dataset, self.missing_dataset = prep.split_complete_data(self.proc_dataset)
        self.numeric_dataset, self.char_dataset = prep.split_features_by_type(self.proc_dataset)
        # self.num_complete_dataset, self.num_missing_dataset = prep.split_complete_data(self.numeric_dataset)
        # self.char_complete_dataset, self.char_missing_dataset = prep.split_complete_data(self.char_dataset)

    def update_stats(self):
        if self.dataset.empty:
            self.lbl_total_samples.setText('0')
            self.lbl_total_features.setText('0')
            self.lbl_complete_samples.setText('0')
            self.lbl_character_features.setText('0')
            self.lbl_numeric_features.setText('0')
            self.lbl_missing_samples.setText('0')
            self.lbl_num_complete.setText('0')
            self.lbl_num_missing.setText('0')
            self.lbl_char_complete.setText('0')
            self.lbl_char_missing.setText('0')
        else:
            self.lbl_total_samples.setText(str(self.proc_dataset.shape[0]))
            self.lbl_total_features.setText(str(self.proc_dataset.shape[1]))
            self.lbl_complete_samples.setText(str(self.complete_dataset.shape[0]))
            self.lbl_character_features.setText(str(self.char_dataset.shape[1]))
            self.lbl_numeric_features.setText(str(self.numeric_dataset.shape[1]))
            self.lbl_missing_samples.setText(str(self.missing_dataset.shape[0]))
            # self.lbl_num_complete.setText(str(self.num_complete_dataset.shape[0]))
            # self.lbl_num_missing.setText(str(self.num_missing_dataset.shape[0]))
            # self.lbl_char_complete.setText(str(self.char_complete_dataset.shape[0]))
            # self.lbl_char_missing.setText(str(self.char_missing_dataset.shape[0]))

            self.fill_feature_table()


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
                    # item.setFlags(QtCore.Qt.ItemIsEnabled)
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
        # color observed column yellow       
        if self.observed_index >= 0:
            for row in range(self.file_table.rowCount()):
                item = self.file_table.item(row, self.observed_index)
                item.setBackground(QtGui.QBrush(QtCore.Qt.yellow))
                # text = str(item.text())
                # if (text.isdigit() and int(text) >= 20) or text == 'WARNING':
        self.file_table.setAlternatingRowColors(True)
        self.file_table.setStyleSheet("alternate-background-color: lightGray;background-color: white;")

    def fill_feature_table(self):
        if not self.proc_dataset.empty:
            # making a table of features
            self.feature_table.setColumnCount(2)  # rows and columns of table
            self.feature_table.setRowCount(self.proc_dataset.shape[1])
            for row in range(self.proc_dataset.shape[1]):
                    item = QTableWidgetItem(
                        str(self.proc_dataset.columns[row]))  # each item is a QTableWidgetItem
                    self.feature_table.setItem(row, 0, item)
                    item = QTableWidgetItem( 
                        prep.series_type(self.proc_dataset[self.proc_dataset.columns[row]])[0:1])
                    # item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.feature_table.setItem(row, 1, item)
            # making cells read-only
            self.feature_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            #making it only possible to select rows
            self.feature_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
            # setting header labels
            self.feature_table.setHorizontalHeaderLabels(['Features','Type'])
            # update colorcodes
            self.repaint_feature_table()

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
