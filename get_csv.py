import sys, csv
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#  pyqtSignal, QObject, Qt, QDate
import datetime
from functools import partial

class Communicate(QObject):

    saveApp =       pyqtSignal()
    updatedateApp = pyqtSignal()
    # tablesignal =   pyqtSignal()


class UI_Window(QMainWindow):

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

        self.c = Communicate()
        self.c.saveApp.connect(self.content.handleSave)
        # self.c.updatedateApp.connect(self.content.getInteger)


        self.openAct = QAction('Open', self)
        self.openAct.setShortcut('Ctrl+O')
        self.openAct.setStatusTip('Open file, looping multiple instances not recommended, only for minimal changes.')
        self.openAct.triggered.connect(self.content.handleOpen)

        self.saveAct = QAction('Save', self)
        self.saveAct.setShortcut('Ctrl+S')
        self.saveAct.setStatusTip('Save file')
        self.saveAct.triggered.connect(self.content.handleSave)


        # self.exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        # self.exitAct.setShortcut('Ctrl+Q')
        # self.exitAct.setStatusTip('Exit application')
        # self.exitAct.triggered.connect(qApp.quit)


        self.menubar = self.menuBar()

        self.fileMenu = self.menubar.addMenu('&File')
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        # self.fileMenu.addAction(self.exitAct)


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

            self.c.saveApp.emit()
            if self.content.saved == 1:
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()


class Content(QWidget):

    def __init__(self, rows, columns):
        super().__init__()

        # self.calendar = Calendar()
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

        for row in range(rows):
            if row == 0:
                self.table.setItem(0,0,QTableWidgetItem('Eric Yung'))
                self.table.setItem(0,1,QTableWidgetItem('14:00'))         # select
                self.table.setItem(0,2,QTableWidgetItem('2'))             # select
                self.table.setItem(0,3,QTableWidgetItem('10-15'))         # calendar
                # self.table.setItem(0,4,QTableWidgetItem('20-01'))         # calendar
                self.table.setItem(0,4,QTableWidgetItem('14:00-16:00'))   # time range
                self.table.setItem(0,5,QTableWidgetItem('FoTan/ YauMaTei/ ShekMun'))             # selection

            else:
                for column in range(columns):

                    if column == 3:

                        btn = QPushButton('Choose Time')
                        self.table.setCellWidget(row, column, btn)

                        btn.clicked.connect(partial(self.calendar, row, column))

                        # def signal_index(self):
                        #     si = pyqtSignal()
                        #     si.connect()

                        # self.table.setItem(row, column, QTableWidgetItem(date.toString()))

                        # connect(tableView, SIGNAL(clicked(const QModelIndex &)), this, SLOT(onTableClicked(const QModelIndex &)));


                    # elif column == 4:

                        # self.table.setItem(row, column, self.lbl)

                    elif column == 5:

                        combo = QComboBox()
                        combo.addItem('')
                        combo.addItem("FoTan")
                        combo.addItem("YauMaTei")
                        combo.addItem("ShekMun")

                        self.table.setCellWidget(row, column, combo)
                    else:
                        item = QTableWidgetItem('')
                        self.table.setItem(row, column, item)
                        # self.table.addAction()

        self.datelabel = QLabel('Date:')
        self.datelabel.setFont(QFont('SansSerif', 14))
        self.time_of_the_day = QLabel('%s' %datetime.datetime.now().date())
        self.time_of_the_day.setFont(QFont('SansSerif', 14))

        self.locationlabel = QLabel("Centre:")
        self.locationlabel.setFont(QFont('SansSerif', 14))
        self.location = QComboBox()
        self.location.setFont(QFont('SansSerif', 14))
        self.location.addItem('')
        self.location.addItem("FoTan")
        self.location.addItem("YauMaTei")
        self.location.addItem("ShekMun")

        self.vbox1 = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox_firstlay = QHBoxLayout()

        # self.vbox1.addStretch(1)
        # self.hbox_firstlay.addStretch(0.5)
        self.hbox_firstlay.addWidget(self.datelabel)
        self.hbox_firstlay.addWidget(self.time_of_the_day)
        self.hbox_firstlay.addStretch(0.5)
        # self.hbox_firstlay.addSpacing(50)
        self.hbox_firstlay.addWidget(self.locationlabel)
        self.hbox_firstlay.addWidget(self.location)

        self.vbox1.addLayout(self.hbox_firstlay)

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
                for row in range(0, self.table.rowCount()):


                    if row == 0:
                        rowdata = []
                        rowdata.extend(('Name', 'Starting Time', 'Duration', 'Booking Date', 'Booking Time', 'Booking Location'))
                        rowdata.append('%s' %self.time_of_the_day.text())
                        rowdata.append('%s' %['', 'F', 'Y', 'S'][self.location.currentIndex()])
                        writer.writerow(rowdata)


                    else:
                        rowdata = []
                        for column in range(self.table.columnCount()):


                            if column == 5:

                                item = self.table.cellWidget(row, column)

                                # this is setting the location
                                if item is not None and str(item.currentIndex()) == '0':
                                    rowdata.append('')
                                elif str(item.currentIndex()) == '1':
                                    rowdata.append("F")
                                elif str(item.currentIndex()) == '2':
                                    rowdata.append('Y')
                                else:
                                    rowdata.append('S')

                            elif column == 3:

                                item = self.table.cellWidget(row, column)

                                # this is setting the location
                                if str(item.text()) != 'Choose Time':
                                    rowdata.append(str(item.text()))
                                elif str(item.text()) == 'Choose Time':
                                    rowdata.append('')
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

    def calendar(self, row, column):

        d = QDialog()
        vbox1 = QVBoxLayout()

        self.cal = QCalendarWidget()
        self.cal.setGridVisible(True)

        # date = self.cal.selectedDate()
        # cal.clicked[QDate].connect(self.showDate(date))

        self.cal.clicked[QDate].connect(partial(self.trigger_signal, row, column))
        # date =

        # def trigger_signal(self):

        #     # determine when to trigger
        #     trigger = pyqtSignal()

        #     # connect to the handle trigger function in self.table
        #     self.trigger.connect(self.handle_trigger)

        vbox1.addWidget(self.cal)

        # self.lbl = QLabel(self)
        # self.lbl.setText(date.toString())
        # vbox1.addWidget(self.lbl)

        d.setLayout(vbox1)
        d.exec_()

    def trigger_signal(self, row, column):
        self.date = self.cal.selectedDate()
        print(self.date)
        # date = cal
        self.table.setItem(row, column, QTableWidgetItem(self.date.toString()))
        print(self.date.toString())




    # def showDate(self, date, row,column):


    # def getInteger(self, row, column):
    #     i, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 28, 0, 100, 1)
    #     if okPressed:
    #         self.integer = i
    #         self.row = row
    #         self.column = column
    #         self.e.updatedateApp.emit()


    # def updateInteger(self):

    #     self.table.setItem(self.row, self.column, QTableWidgetItem(self.integer))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = UI_Window()
    sys.exit(app.exec_())