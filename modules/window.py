import sys
sys.path.append(".\\modules")
from script import *

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QProgressBar)
from PyQt5.QtCore import pyqtSignal, QObject, QPoint
    


class ProgressWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initProgressWindow()


    def initProgressWindow(self):
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(QApplication.instance().quit)
        hboxManage = QHBoxLayout()
        hboxManage.addStretch(1)
        hboxManage.addWidget(cancelButton)
        
        progress=QProgressBar()
        hboxProgress=QHBoxLayout()
        #hboxProgress.addStretch(1)
        hboxProgress.addWidget(progress)
        
        self.label=QLabel("In progress:")
        self.hboxDescription=QHBoxLayout()
        self.hboxDescription.addWidget(self.label)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(self.hboxDescription)
        vbox.addStretch(1)
        vbox.addLayout(hboxProgress)
        vbox.addStretch(1)
        vbox.addLayout(hboxManage)
        self.setLayout(vbox)    
        self.setGeometry(300, 300, 400, 250)
        self.setMinimumSize(400, 250)
        self.setMaximumSize(400, 250)
        self.setWindowTitle('In progress...')    
        self.show()

    
    
    
class FirstWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.secondWin = None
        self.initUI()


    def initUI(self):
        
        addButton1=QPushButton("Add")
        
        addButton2=QPushButton("Add")
        
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")
        
        self.label1=QLabel('Enter the ID.\nPress the "Add" button and enter the ID or short adress of VK user\nThen press "OK"')
        self.line1=QLineEdit("First ID")
        self.line2=QLineEdit("Second ID")
        self.line1.setReadOnly(True)
        self.line2.setReadOnly(True)
        
        addButton1.clicked.connect(self.setTheId1)
        addButton2.clicked.connect(self.setTheId2)
        okButton.clicked.connect(self.OK)
        cancelButton.clicked.connect(QApplication.instance().quit)
        
        hboxManage = QHBoxLayout()
        hboxManage.addStretch(1)
        hboxManage.addWidget(okButton)
        hboxManage.addWidget(cancelButton)
        
        hboxTheLabel=QHBoxLayout()
        hboxTheLabel.addWidget(self.label1)
        
        hboxFirstLine=QHBoxLayout()
        hboxFirstLine.addWidget(self.line1)
        hboxFirstLine.addWidget(addButton1)
        
        hboxSecondLine=QHBoxLayout()
        hboxSecondLine.addWidget(self.line2)
        hboxSecondLine.addWidget(addButton2)
        
        vboxDescription=QVBoxLayout()
        vboxDescription.addLayout(hboxTheLabel)
        
        
        vboxMainArea=QVBoxLayout()
        vboxMainArea.addLayout(hboxFirstLine)
        vboxMainArea.addLayout(hboxSecondLine)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(vboxDescription)
        vbox.addStretch(1)
        vbox.addLayout(vboxMainArea)
        vbox.addStretch(1)
        vbox.addLayout(hboxManage)
        
        
        self.setLayout(vbox)    
        
        self.setGeometry(300, 300, 400, 250)
        self.setMinimumSize(400, 250)
        self.setMaximumSize(400, 250)
        self.setWindowTitle('Let`s start!')    
        self.show()
        
    

    def setTheId1(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Enter the ID:')

        if ok:
            self.line1.setText(str(text))
            self.line1_val=str(text)
    
    def setTheId2(self):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Enter the ID:')

        if ok:
            self.line2.setText(str(text))
            self.line2_val=str(text)
            
            
    def OK(self):
        
        self.close()
        if not self.secondWin:
            self.secondWin=ProgressWindow()
        #main(self.line1_val, self.line2_val)
        
    



def GUI():
    app = QApplication(sys.argv)
    
    ex = FirstWindow()
    
    sys.exit(app.exec_())