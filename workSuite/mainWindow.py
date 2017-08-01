#encoding: utf-8
import os
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from processor import *

__version__ = '1.0.0'

class mainWindow(QtGui.QWidget):

    processor = None
    loadDir = None

    def __init__(self, parent=None):
        super(mainWindow, self).__init__(parent)

        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 500, 200)
        self.setWindowTitle('Mom work tool v0.1')

        self.quit = QtGui.QPushButton('Close', self)
        self.quit.setGeometry(10, 10, 70, 40)
        # new pyQt4, good standard, clean, more intuitive
        self.quit.clicked.connect(QtGui.QApplication.quit)

        self.openFile = QtGui.QPushButton('Open', self)
        self.openFile.setGeometry(80,10,70,40)
        self.openFile.clicked.connect(self.on_openFile_clicked)

        self.extracting = QtGui.QPushButton('Extract', self)
        self.extracting.setGeometry(150, 10, 70, 40)
        self.extracting.clicked.connect(self.on_extracting_clicked)

        self.extracting = QtGui.QPushButton('Save', self)
        self.extracting.setGeometry(220, 10, 70, 40)
        self.extracting.clicked.connect(self.on_saveFile_clicked)

        self.text = QLabel(self)
        self.text.move(10,100)
        self.text.resize(500,40)
        self.text.setText("Welcome!")

        #WARNING: this is an old school standard : DO NOT USE SUCH STYLE
        # self.connect(quit, QtCore.SIGNAL('clicked'), QtGui.qApp, QtCore.SLOT('quit()'))

    #open an target file
    def on_openFile_clicked(self):
        self.loadDir = QFileDialog.getOpenFileName(self, 'Open File')
        try:
            if self.loadDir.split('.')[-1] != 'txt':
                self.text.setText("Error! Only .txt file is acceptable.")
            else:
                openFile = open(self.loadDir)
                #initialize a processor class
                self.processor = processor()
                contents = openFile.readlines()
                self.processor.setContents(contents)
                self.text.setText("Successfully opened {0}".format(self.loadDir))
        except:
            self.text.setText("Unexpected error!")

    #process file
    def on_extracting_clicked(self):
        self.processor.process()
        self.text.setText("Successfully processed.")

    #save file
    def on_saveFile_clicked(self):
        # return self.processor.processed
        name = QFileDialog.getSaveFileName(self, 'Save File')
        return self.processor.processed.to_csv(path_or_buf=name)

def main():
    app = QtGui.QApplication(sys.argv)
    dw = mainWindow()
    dw.show()
    sys.exit(app.exec_())
