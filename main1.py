from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 819)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.UploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.UploadButton.setGeometry(QtCore.QRect(340, 110, 141, 41))
        self.UploadButton.setStyleSheet("font: 75 italic 14pt \"Palatino Linotype\";")
        self.UploadButton.setObjectName("UploadButton")

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(70, 260, 681, 151))
        self.tableWidget.setObjectName("tableWidget")

        self.filelabel = QtWidgets.QLabel(self.centralwidget)
        self.filelabel.setGeometry(QtCore.QRect(350, 190, 300, 41))
        self.filelabel.setStyleSheet("font: 10pt \"MS Reference Sans Serif\";")
        self.filelabel.setObjectName("filelabel")

        self.SearchLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.SearchLineEdit.setGeometry(QtCore.QRect(60, 440, 181, 31))
        self.SearchLineEdit.setObjectName("SearchLineEdit")

        self.SearchButton = QtWidgets.QPushButton(self.centralwidget)
        self.SearchButton.setGeometry(QtCore.QRect(260, 440, 93, 31))
        self.SearchButton.setStyleSheet("font: 9pt \"Mongolian Baiti\";")
        self.SearchButton.setObjectName("SearchButton")

        self.resultBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.resultBrowser.setGeometry(QtCore.QRect(50, 520, 721, 192))
        self.resultBrowser.setObjectName("resultBrowser")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect buttons to functions
        self.UploadButton.clicked.connect(self.load_file)
        self.SearchButton.clicked.connect(self.search_value)

        self.df = pd.DataFrame()  # Placeholder for the loaded DataFrame

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Viewer"))
        self.UploadButton.setText(_translate("MainWindow", "Upload File"))
        self.filelabel.setText(_translate("MainWindow", "No file selected"))
        self.SearchLineEdit.setPlaceholderText(_translate("MainWindow", "Enter the value to search.."))
        self.SearchButton.setText(_translate("MainWindow", "Search"))

    def load_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Open File",
            "",
            "Data Files (*.csv *.xlsx *.xls)"
        )
        if file_path:
            self.filelabel.setText(os.path.basename(file_path))
            try:
                if file_path.endswith(".csv"):
                    self.df = pd.read_csv(file_path)
                elif file_path.endswith((".xlsx", ".xls")):
                    self.df = pd.read_excel(file_path)
                else:
                    self.resultBrowser.setText("Unsupported file format.")
                    return
                self.display_data()
            except Exception as e:
                self.resultBrowser.setText(f"Error loading file:\n{str(e)}")

    def display_data(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        if not self.df.empty:
            self.tableWidget.setColumnCount(len(self.df.columns))
            self.tableWidget.setHorizontalHeaderLabels(self.df.columns)
            self.tableWidget.setRowCount(len(self.df.index))
            for i in range(len(self.df.index)):
                for j in range(len(self.df.columns)):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(self.df.iat[i, j])))

    def search_value(self):
        query = self.SearchLineEdit.text().strip()
        if not query or self.df.empty:
            self.resultBrowser.setText("Please upload a file and enter a search term.")
            return
        results = self.df[self.df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
        if results.empty:
            self.resultBrowser.setText("No matching results found.")
        else:
            self.resultBrowser.setText(results.to_string(index=False))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())