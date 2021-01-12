from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, QtCore
import pymysql
import ast


def MyConverter(mydata):
    def cvt(data):
        try:
            return ast.literal_eval(data)

        except Exception:
            return str(data)
    return tuple(map(cvt, mydata))


class Component(QDialog):
    def __init__(self):
        super().__init__()
        self.inItUi()
        self.loadData()

    # =========== Database connection function =================
    def loadData(self):
        # db = pymysql.connect(host='35.223.238.107', user='root', password='aryabhat', database='Component')
        db = pymysql.connect(host='localhost', user='root', password='', database='testdb')
        with db:
            cur = db.cursor()
            cur.execute("select Name,formula from mytable")
            data = cur.fetchall()

            for row in data:
                self.addTable(MyConverter(row))

            cur.close()

    def addTable(self, columns):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)

        for i, column in enumerate(columns):
            self.tableWidget.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(column)))

    def inItUi(self):
        self.resize(271, 269)
        self.widget = QWidget(self)
        self.widget.setGeometry(QtCore.QRect(10, 10, 251, 251))
        self.widget.setObjectName("widget")

        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.tableWidget = QTableWidget(self.widget)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")

        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)

        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)

        self.verticalLayout.addWidget(self.tableWidget)
        self.add_row = QPushButton(self.widget)
        self.add_row.setText("Add Row")
        self.verticalLayout.addWidget(self.add_row)
        self.del_row = QPushButton(self.widget)
        self.del_row.setText("Delete row")
        self.verticalLayout.addWidget(self.del_row)

        self.setWindowTitle("Components")
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText("Formula")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText("Formula Type")
