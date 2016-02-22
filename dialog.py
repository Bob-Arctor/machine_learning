import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog, QTableWidgetItem
import pandas as pd

form_class = uic.loadUiType("gui.ui")[0]  # Load the UI


class MyWindowClass(QtGui.QWidget, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btn_load.clicked.connect(self.btn_load_clicked)  # Bind the event handlers
        self.btn_select_file.clicked.connect(self.selectFile)

        self.filepath = ''
        self.dataset = pd.DataFrame()

    def btn_load_clicked(self):  # read csv file
        self.createProgressBar()
        self.dataset = pd.read_csv(self.lineEdit_filepath.text())
        self.filepath = self.lineEdit_filepath.text()
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
        self.progressBar.show()

    def fill_data_table(self):
        if len(self.filepath):
            self.file_table.setColumnCount(self.dataset.shape[1])  # rows and columns of table
            self.file_table.setRowCount(self.spin_head.value())
            total = self.dataset.shape[1] + self.spin_head.value()
            counter = 0
            for row in range(self.spin_head.value()):  # add items from array to QTableWidget
                for column in range(self.dataset.shape[1]):
                    item = QTableWidgetItem(
                        str(self.dataset[self.dataset.columns[column]][row]))  # each item is a QTableWidgetItem
                    #item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.file_table.setItem(row, column, item)
                    counter += 1
                    self.progressBar.setValue(int(counter // total))
            # making cells read-only
            self.file_table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
            # setting header labels
            self.file_table.setHorizontalHeaderLabels(list(self.dataset.columns))

            self.progressBar.hide()


app = QtGui.QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
app.exec_()
