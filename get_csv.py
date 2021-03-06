import csv
import sys
import datetime
from functools import partial


from PyQt5.QtCore import pyqtSignal, QDate, Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget, QTableWidget, QCalendarWidget,
    QTableWidgetItem, QDialog,
    QAction, QComboBox, QFileDialog, QLabel, QMessageBox, QPushButton, QToolTip,
    QHeaderView, QHBoxLayout, QVBoxLayout,
)


class UI_Window(QMainWindow):

    saveApp = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.no_std = 40

        # number of rows and columns
        self.content = Content(self.no_std, 6)
        self.setCentralWidget(self.content)

        self.statusBar()
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setToolTip('Click a box and fill in your info')

        self.saveApp.connect(self.content.handleSave)

        openAct = QAction('Open', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open file, looping multiple instances not recommended, only for minimal changes.')
        openAct.triggered.connect(self.content.handleOpen)

        saveAct = QAction('Save', self)
        saveAct.setShortcut('Ctrl+S')
        saveAct.setStatusTip('Save file')
        saveAct.triggered.connect(self.content.handleSave)

        # exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        # exitAct.setShortcut('Ctrl+Q')
        # exitAct.setStatusTip('Exit application')
        # exitAct.triggered.connect(qApp.quit)

        self.menubar = self.menuBar()

        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(openAct)
        self.fileMenu.addAction(saveAct)
        # self.fileMenu.addAction(exitAct)

        self.setGeometry(300, 300, 1440, 1200)
        self.setWindowTitle('Timesheet')
        self.setWindowIcon(QIcon('web.png'))
        self.show()

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
            "Do you want to save?", QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)

        if reply == QMessageBox.Discard:
            event.accept()
        elif reply == QMessageBox.Save:

            self.saveApp.emit()
            if self.content.saved == 1:
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()


class Content(QWidget):
    def __init__(self, rows, columns):
        super().__init__()

        self.table = QTableWidget(rows, columns, self)
        self.table.setHorizontalHeaderLabels(['Name', 'Starting Time', 'Duration (Hrs)', 'Booking Date (MM-DD)', 'Booking Time', 'Booking Location'])

        header = self.table.horizontalHeader()
        header.setFont(QFont('SansSerif', 14))
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        b = ['Student' for j in range(1,rows)]
        b.insert(0, 'Example')
        self.table.setVerticalHeaderLabels(b)

        # index = self.table.verticalHeader()
        # for i in range(rows):
        #     index.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        # self.table.setSelection
        self.table.setFont(QFont('SansSerif', 12))

        self.table.setItem(0,0,QTableWidgetItem('Eric Yung'))
        self.table.setItem(0,1,QTableWidgetItem('14:00'))         # select
        self.table.setItem(0,2,QTableWidgetItem('2'))             # select
        self.table.setItem(0,3,QTableWidgetItem('Click below to choose'))         # calendar
        # self.table.setItem(0,4,QTableWidgetItem('20-01'))         # calendar
        self.table.setItem(0,4,QTableWidgetItem('14:00-16:00'))   # time range
        self.table.setItem(0,5,QTableWidgetItem('FoTan/ YauMaTei/ ShekMun'))             # selection

        # Todo: Replace hardcoded columns with variables
        for row in range(1,rows):
            # Set empty text boxes
            empty_text_cols = (0, 1, 2, 4)   # hardcode
            for col in empty_text_cols:
                item = QTableWidgetItem('')
                self.table.setItem(row, col, item)

            # Set column 3 calender button
            btn = QPushButton('Choose Time')
            btn.clicked.connect(partial(self.showCalendar, row))
            self.table.setCellWidget(row, 3, btn)  # hardcode

            # Set column 5 location dropdown list
            combo = QComboBox()
            combo.addItem('')  # use n/a?
            combo.addItem("FoTan")
            combo.addItem("YauMaTei")
            combo.addItem("ShekMun")
            self.table.setCellWidget(row, 5, combo)  # hardcode

        datelabel = QLabel('Date:')
        datelabel.setFont(QFont('SansSerif', 14))
        time_of_the_day = QLabel('%s' %datetime.datetime.now().date())
        time_of_the_day.setFont(QFont('SansSerif', 14))

        locationlabel = QLabel("Centre:")
        locationlabel.setFont(QFont('SansSerif', 14))
        location = QComboBox()
        location.setFont(QFont('SansSerif', 14))
        location.addItem('')
        location.addItem("FoTan")
        location.addItem("YauMaTei")
        location.addItem("ShekMun")

        # Todo(alan): consider making this a class attr
        self.location_labels = ('', 'F', 'Y', 'S')

        # Todo(alan): refactor these attrs?
        self.time_of_the_day = time_of_the_day
        self.location = location

        self.vbox1 = QVBoxLayout()
        self.hbox = QHBoxLayout()
        hbox_firstlay = QHBoxLayout()

        # self.vbox1.addStretch(1)
        # self.hbox_firstlay.addStretch(0.5)
        hbox_firstlay.addWidget(datelabel)
        hbox_firstlay.addWidget(self.time_of_the_day)
        hbox_firstlay.addStretch(0.5)

        # hbox_firstlay.addSpacing(50)
        hbox_firstlay.addWidget(locationlabel)
        hbox_firstlay.addWidget(self.location)

        self.vbox1.addLayout(hbox_firstlay)

        self.hbox.addWidget(self.table)
        self.vbox1.addLayout(self.hbox)
        # self.vbox1.setStretch(1,1)
        self.setLayout(self.vbox1)

    def handleSave(self):
        path = QFileDialog.getSaveFileName(self, 'Save File', '.csv', 'CSV(*.csv)')[0]

        # saved flap for smoother terminating
        self.saved = 0
        try:
            with open(path, 'w', encoding='big5-hkscs') as stream:
                writer = csv.writer(stream)

                rowdata = []
                rowdata.extend(('Name', 'Starting Time', 'Duration', 'Booking Date', 'Booking Time', 'Booking Location'))
                rowdata.append('%s' % self.time_of_the_day.text())
                rowdata.append('%s' % self.location_labels[self.location.currentIndex()])
                writer.writerow(rowdata)

                for row in range(1, self.table.rowCount()):
                    rowdata = []
                    for column in range(self.table.columnCount()):
                        if column == 5:
                            item = self.table.cellWidget(row, column)

                            # this is setting the location
                            if item is not None:
                                rowdata.append(self.location_labels[item.currentIndex()])
                            else:
                                rowdata.append('')

                        elif column == 3:
                            item = self.table.cellWidget(row, column)

                            # this is setting the location
                            if item.text() != 'Choose Time':
                                rowdata.append(item.text())
                            else:
                                rowdata.append('')

                        else:
                            item = self.table.item(row, column)
                            if item is not None and str(item.text()) != 'Enter':
                                rowdata.append(str(item.text()))
                            elif str(item.text()) == 'Enter':
                                rowdata.append('')
                            else:
                                rowdata.append('')
                    writer.writerow(rowdata)

            self.saved = 1
            # self.e.updatedateApp.emit()
        except FileNotFoundError:
            pass

    def handleOpen(self):
        path = QFileDialog.getOpenFileName(self, 'Open File', '.csv', 'CSV(*.csv)')[0]

        try:
            with open(path, 'r', encoding='big5-hkscs') as stream:
                self.table.setRowCount(0)
                self.table.setColumnCount(0)
                for rowdata in csv.reader(stream):
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    self.table.setColumnCount(len(rowdata))
                    for column, data in enumerate(rowdata):
                        # data = QTableWidgetItem(data)
                        if column == 5:
                            if data == "F":
                                data = "FoTan"
                            elif data == "Y":
                                data = "YauMaTei"
                            elif data == "S":
                                data = "ShekMun"
                            else:
                                data = 'Enter'
                            combo = QComboBox()
                            combo.addItem('Enter')
                            combo.addItem("FoTan")
                            combo.addItem("YauMaTei")
                            combo.addItem("ShekMun")
                            self.table.setCellWidget(row, column, combo)

                            index = combo.findText(data, Qt.MatchFixedString)
                            combo.setCurrentIndex(index)

                        else:
                            item = QTableWidgetItem(data)
                            self.table.setItem(row, column, item)
        except FileNotFoundError:
            pass

    def showCalendar(self, row):
        dialog = QDialog()
        vbox1 = QVBoxLayout()

        cal = QCalendarWidget()
        cal.setGridVisible(True)

        dialog.setToolTip('Double-click to confirm')

        # single click
        cal.clicked[QDate].connect(partial(self.setDate, row, cal))
        # double click
        cal.activated[QDate].connect(partial(self.setDateAndClose, row, cal, dialog))

        vbox1.addWidget(cal)

        dialog.setLayout(vbox1)
        dialog.exec()

    def setDate(self, row, cal):
        date = cal.selectedDate()
        self.table.cellWidget(row, 3).setText((date.toString()))

    def setDateAndClose(self, row, cal, dialog):
        self.setDate(row, cal)
        dialog.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UI_Window()
    sys.exit(app.exec())
