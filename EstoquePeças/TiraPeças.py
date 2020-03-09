from PySide2 import QtUiTools
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QFile
from PySide2.QtWidgets import *
import sys
import ctypes
import pyodbc
from PySide2.QtGui import QIcon
from pathlib import Path
import datetime
import xlwt
import os.path

hoje = datetime.date.today()
mes = hoje.month
ano = hoje.year
dia = hoje.day


class UI_MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self, parent=None)

        telacheia = ctypes.windll.user32

        file = QtCore.QFile('TiraPeças.ui')
        file.open(QFile.ReadOnly)

        carregador = QtUiTools.QUiLoader()

        self.ui = carregador.load(file)

        grid_layout = QGridLayout()
        grid_layout.addWidget(self.ui)
        grid_layout.setMargin(0)

        self.setLayout(grid_layout)

        self.setMaximumSize(QtCore.QSize(telacheia.GetSystemMetrics(0), telacheia.GetSystemMetrics(1)))
        self.setGeometry(telacheia.GetSystemMetrics(0) - telacheia.GetSystemMetrics(0)+8 , telacheia.GetSystemMetrics(1) - telacheia.GetSystemMetrics(1) + 31, telacheia.GetSystemMetrics(0) - 16, telacheia.GetSystemMetrics(1) - 77)

        self.servidor = "MACROSUL-BTESTE\SQLEXPRESS"
        self.banco = "DB_desm"
        self.login = "sa"
        self.senha = "m@crosul"
        self.servidorof = "Driver={SQL Server Native Client 11.0};Server=" + self.servidor + ';Database=' + self.banco + ';UID=' + \
                          self.login + ';PWD=' + self.senha

        self.connection = pyodbc.connect(self.servidorof)

    def inserir(self):
        itemcode = self.ui.ENT_codigosap.text().upper()
        consulta = self.consulta(itemcode)

        inserindo = "insert into PCS1(itemcode, compretirado, tdate, Cliente, Utilização, Responsavel, invstatus) values('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format()
        cursor = self.connection.cursor()

        # verificando de a busca não é nula
        if cursor is not None:
            cursor.execute(inserindo)
            cursor.commit()
            cursor.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    window = UI_MainWindow()
    window.show()
    app.exec_()