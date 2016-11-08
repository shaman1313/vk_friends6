from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QProgressBar, QMessageBox, QCheckBox)
from PyQt5.QtCore import pyqtSignal, QObject, QPoint, QThread, pyqtSlot, Qt


import sys
import os
import time
import webbrowser
sys.path.append(".\\modules")
sys.path.append("..\\friends\\modules")
from function import *
from window import *
    
class ProgressThread(QThread):
    prog=pyqtSignal(int)
    task=pyqtSignal(str)
    msg=pyqtSignal(str)
    
    
    def __init__(self, one, two):
        super().__init__()
        self.firstId=one
        self.secondId=two
    def run(self):
        
        whoAmI=self.firstId          
        whoIsSome=self.secondId
        flag=True
        print (whoAmI)
        print (whoIsSome)
        
        f=open("isUser.xml", 'w', encoding='utf-8')
        f.close()
        f=open("friends.xml", 'w', encoding='utf-8')
        f.close()
        f=open("person.xml", 'w', encoding='utf-8')
        f.close()
        
        
        firstP_id=isIdAndConvert(whoAmI)
        secondP_id=isIdAndConvert(whoIsSome)
                
        contact=''  #contact is list of mutual elements between friendlists
                    #it used for build connection table

        listOfFr_1p_lay1=getListOfFriends(firstP_id)
        print("In layer 1 are %d entries for P1" % len(listOfFr_1p_lay1))
        mn_listOfFr_1p=set(listOfFr_1p_lay1)

        if secondP_id in mn_listOfFr_1p:
            print ('Second person is your friend!') #checking if P2 is friend of P1
            self.msg.emit('Second person is your friend!')
            self.prog.emit(100)
            flag=False          ######## Exit if Match results
        else:

            listOfFr_2p_lay1=getListOfFriends(secondP_id) #get friendlist for 2nd person (layer 1)
            print("In layer 1 are %d entries for P2" % len(listOfFr_2p_lay1))

            #Checking for mutual fr in layer1
            mn_listOfFr_2p=set(listOfFr_2p_lay1)
            mn_betw11=mn_listOfFr_1p & mn_listOfFr_2p #mutual elements in friendlists of P1 and P2 
            
            if len(list(mn_betw11))!=0: #if you have mutual elements, build connection table
                print ('You have %d mutual friends' % len(list(mn_betw11)))
                contact=list(mn_betw11)
                connection_table=[]
                

                #building the chains and add it to conn. table for each of mutual elements 
                iter=0
                for member in contact:
                    iter+=1
                    chain=[firstP_id, member, secondP_id]
                    connection_table.append(chain)
                    self.prog.emit(int(iter/len(contact)*100))
                    self.task.emit('Building the chains')
                    
                print('\n%d chains were build:' % len(connection_table))
                
            else:   #if you do not have mutual friends in layer 1
                self.task.emit('Downloading info for layer2 (person 1):')

                listOfFr_1p_lay2=[]##friendslist of L2 for P1
                i=0     #iterator for progress indication
                for member in listOfFr_1p_lay1:#for each ID 
                    listOfFr_1p_lay2.extend(getListOfFriends(member))
                    i+=1
                    self.prog.emit(int(i/len(listOfFr_1p_lay1)*100))
                    
                print("\nIn layer 2 are %d entries for P1" % len(listOfFr_1p_lay2))
                mn_listOfFr_1p_l2=set(listOfFr_1p_lay2)##friendslist of L2 for P1
                mn_betw21=mn_listOfFr_1p_l2 & mn_listOfFr_2p#### the difference between L2P1 and L1P2
                
                
                if len(list(mn_betw21)) != 0:#if you have mutual elements, build connection table
                    print ('You have %d mutual friends' % len(list(mn_betw21)))
                    contact=list(mn_betw21)
                    connection_table=[]
                    #building the chains and add it to conn. table for each of mutual elements 
                    iter=0
                    for member in contact:#for each member in contact 
                        iter+=1
                        working_FrList=getListOfFriends(member)#get list of friends
                        contakt_w_l=set(working_FrList) & mn_listOfFr_1p#search mutual elements between fr list and layer 1 person 1
                        for cont in contakt_w_l:##for each member in this list form the chains and connection table
                            chain=[firstP_id, cont, member, secondP_id]
                            connection_table.append(chain)
                        self.prog.emit(int(iter/len(contact)*100))
                        self.task.emit('Building the chains')
                    print('\n%d chains were build:' % len(connection_table))
                    
                else:
                    print('Downloading info for layer2 (person 2):')
                    self.task.emit('Downloading info for layer2 (person 2)')
                    listOfFr_2p_lay2=[]
                    i=0
                    for member in listOfFr_2p_lay1:#for each ID 
                        listOfFr_2p_lay2.extend(getListOfFriends(member))
                        i+=1
                        self.prog.emit(int(i/len(listOfFr_1p_lay1)*100))
                    print("\nIn layer 2 are %d entries for P2" % len(listOfFr_2p_lay2))
                    mn_listOfFr_2p_l2=set(listOfFr_2p_lay2)##friendslist of L2 for P2
                    mn_betw22=mn_listOfFr_1p_l2 & mn_listOfFr_2p_l2#### the difference between L2P1 and L2P2
                    
                    if len(list(mn_betw22)) != 0:
                        print ('You have %d mutual friends' % len(list(mn_betw22)))
                        contact=list(mn_betw22)
                        connection_table=[]
                        #building the chains and add it to conn. table for each of mutual elements 
                        self.task.emit("Building the chains")
                        iter=0
                        for member in contact:#for each member in contact 
                            iter+=1
                            working_FrList=getListOfFriends(member)#get list of friends
                            contakt_w_p1=set(working_FrList) & mn_listOfFr_1p#search mutual elements between fr list and layer 1 person 1
                            contakt_w_p2=set(working_FrList) & mn_listOfFr_2p#search mutual elements between fr list and layer 1 person 2
                            for cont1 in contakt_w_p1:##for each member in this list form the chains and connection table
                                for cont2 in contakt_w_p2:
                                    chain=[firstP_id, cont1, member, cont2, secondP_id]
                                    connection_table.append(chain)
                            self.prog.emit(int(iter/len(contact)*100))
                        print('\n%d chains were build:' % len(connection_table))
                        
                        
                    else:
                        print ('I`m don`t find any chains')
                        self.msg.emit('I`m don`t find any chains')
                        exiter()
                        flag=False
                        
        if flag:
            result(connection_table)
        #####################################################################################################
        #### Clearing the working directory
            exiter()
        
        self.quit()
        
        
            
class messageWin(QWidget):

    def __init__(self, mess):
        super().__init__()
        self.message=mess
        self.initUI()


    def initUI(self):

        reply = QMessageBox.information(self, 'Message',
            self.message, QMessageBox.Ok, QMessageBox.Ok)
            
class errorWin (QWidget):
    def __init__(self, mess):
        
        super().__init__()
        self.message=mess
        self.initUI()
        
    def initUI(self):
        reply=QMessageBox.critical(self, 'Warning', self.message, QMessageBox.Yes, QMessageBox.Yes)
        

        


    

        
        


          

class ProgressWindow(QWidget):
    
    def __init__(self, one, two):
        super().__init__()
        self.myThread = None
        self.showR=False
        
      
        self.firstId=one
        self.secondId=two
        print (self.firstId, self.secondId)
        self.on_working()
        
        self.initProgressWindow()
        
        
    def on_working(self):
        if not self.myThread:
            self.myThread=ProgressThread(self.firstId, self.secondId)
            self.myThread.prog.connect(self.on_progress)
            self.myThread.task.connect(self.on_task)
            self.myThread.msg.connect(self.thrMsg)
    
            
            self.myThread.finished.connect(self.on_finished)
            self.myThread.start()
            
        
    def on_progress(self, value):
        self.progress.setValue(value)
    def on_task(self, value):
        self.label2.setText(value)
    def thrMsg(self, value):
        message=messageWin(value)
    
    def on_finished(self):
        self.myThread.prog.disconnect(self.on_progress)
        self.myThread.task.disconnect(self.on_task)
        self.myThread.msg.disconnect(self.thrMsg)
        self.myThread.finished.disconnect(self.on_finished)
        self.myThread = None
        print ("thread closed")
        
        self.cancelButton.clicked.disconnect(QApplication.instance().quit)
        self.cancelButton.setText('Done')
        self.cancelButton.clicked.connect(self.done)
        
        self.cb=QCheckBox('Show me the result file', self)
        self.cb.stateChanged.connect(self.showRes)
        
        self.hboxManage.addWidget(self.cb)
        self.messageDone=messageWin('Hell Yeah! Done!')
    
    def done(self):
        if self.showR:
            webbrowser.open('result.html')
            self.close()
        else:
            self.close()
    
    def showRes(self, state):
        if state==Qt.Checked:
            self.showR=True
        else:
            self.showR=False
        
        
            
        
    
    def initProgressWindow(self):
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(QApplication.instance().quit)
        
        
        
        self.hboxManage = QHBoxLayout()
        
        self.hboxManage.addStretch(1)
        self.hboxManage.addWidget(self.cancelButton)
        
        self.progress=QProgressBar()
        hboxProgress=QHBoxLayout()
        hboxProgress.addWidget(self.progress)
        
        vboxProgress=QVBoxLayout()
        vboxProgress.addLayout(hboxProgress)
        
        self.label=QLabel("In progress:")
        self.label2=QLabel('This is process in progress ')
        self.hboxDescription=QHBoxLayout()
        self.hboxDescription.addWidget(self.label)
        
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(self.hboxDescription)
        vbox.addStretch(1)
        vbox.addWidget(self.label2)
        vbox.addLayout(vboxProgress)
        vbox.addStretch(1)
        vbox.addLayout(self.hboxManage)
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
        self.line1_val='319299777'
        self.line2_val='h.victory'

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
        
        
        if len(self.line1_val)==0 or len(self.line2_val)==0:
            error=errorWin('One or more arguments no taken!')
        elif self.line1_val == self.line2_val:
            error=errorWin('Error! The IDs are the same!')
        else:
            self.close()
            if not self.secondWin:
                self.secondWin=ProgressWindow(self.line1_val, self.line2_val)
            
        
        
        
        
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = FirstWindow()
    
    sys.exit(app.exec_())