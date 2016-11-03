from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QProgressBar)
from PyQt5.QtCore import pyqtSignal, QObject, QPoint, QThread, pyqtSlot


import sys
import os
import time
sys.path.append(".\\modules")
sys.path.append("..\\friends\\modules")
from function import *
from window import *
    
class ProgressThread(QThread):
    prog=pyqtSignal(int)
    task=pyqtSignal(str)
    
    
    def __init__(self):
        super().__init__()
    def run(self):########################################Заглушка для процесса работы
        
        whoAmI='319299777'          #ID or short adress of first person
        whoIsSome='alesbelarus'
        #ID or short adress of second person
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
        if firstP_id == secondP_id:
            print ('Error! The IDs are the same!')
            sys.exit()
        start=time.time()
        contact=''  #contact is list of mutual elements between friendlists
                    #it used for build connection table

        listOfFr_1p_lay1=getListOfFriends(firstP_id)
        print("In layer 1 are %d entries for P1" % len(listOfFr_1p_lay1))
        mn_listOfFr_1p=set(listOfFr_1p_lay1)

        if secondP_id in mn_listOfFr_1p:
            print ('Second person is your friend!') #checking if P2 is friend of P1
            sys.exit()          ######## Exit if Match results
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
                for member in contact:
                    chain=[firstP_id, member, secondP_id]
                    connection_table.append(chain)
                    
                print('\n%d chains were build:' % len(connection_table))
                finish=time.time()
                exect=finish-start
                print('On work %.3f seconds\n' % exect)
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
                    for member in contact:#for each member in contact 
                        working_FrList=getListOfFriends(member)#get list of friends
                        contakt_w_l=set(working_FrList) & mn_listOfFr_1p#search mutual elements between fr list and layer 1 person 1
                        for cont in contakt_w_l:##for each member in this list form the chains and connection table
                            chain=[firstP_id, cont, member, secondP_id]
                            connection_table.append(chain)
                    
                    print('\n%d chains were build:' % len(connection_table))
                    finish=time.time()
                    exect=finish-start
                    print('On work %.3f seconds\n' % exect)
                else:
                    print('Downloading info for layer2 (person 2):')
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
                        for member in contact:#for each member in contact 
                            working_FrList=getListOfFriends(member)#get list of friends
                            contakt_w_p1=set(working_FrList) & mn_listOfFr_1p#search mutual elements between fr list and layer 1 person 1
                            contakt_w_p2=set(working_FrList) & mn_listOfFr_2p#search mutual elements between fr list and layer 1 person 2
                            for cont1 in contakt_w_p1:##for each member in this list form the chains and connection table
                                for cont2 in contakt_w_p2:
                                    chain=[firstP_id, cont1, member, cont2, secondP_id]
                                    connection_table.append(chain)
                    
                        print('\n%d chains were build:' % len(connection_table))
                        finish=time.time()
                        exect=finish-start
                        print('On work %.3f seconds\n' % exect)
                        
                    else:
                        print ('I`m don`t find any chains')
                        exiter()
                        sys.exit()
                        

        result(connection_table)
        #####################################################################################################
        #### Clearing the working directory
        exiter()
        finish=time.time()
        exect=finish-start
            

          

class ProgressWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        #firstId=''
        #secondId=''
        self.myThread = None
        self.on_working()
        #id1=pyqtSignal(str)
        #id2=pyqtSignal(str)
        self.initProgressWindow()
        #id1.connect(self.set_id1)
        #id2.connect(self.set_id2)
        
    def on_working(self):
        if not self.myThread:
            self.myThread=ProgressThread()
            self.myThread.prog.connect(self.on_progress)
            self.myThread.task.connect(self.on_task)
            
    
            #self.id1.connect(self.set_id1)
            #self.id2.connect(self.set_id2)
            self.myThread.finished.connect(self.on_finished)
            self.myThread.start()
        
    def on_progress(self, value):
        self.progress.setValue(value)
    def on_task(self, value):
        self.label2.setText(value)
    '''def set_id1(self, value):
        self.firstId=value
    def set_id2(self, value):
        self.secondId=value'''
        
    def on_finished(self):
        self.myThread.prog.disconnect(self.on_progress)
        self.myThread.task.disconnect(self.on_task)
        self.myThread.finished.disconnect(self.on_finished)
        self.myThread = None
    
    def initProgressWindow(self):
        cancelButton = QPushButton("Cancel")
        cancelButton.clicked.connect(QApplication.instance().quit)
        hboxManage = QHBoxLayout()
        hboxManage.addStretch(1)
        hboxManage.addWidget(cancelButton)
        
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
            self.secondWin=ProgressWindow()#############вставить проверку на наличие айдишников!!!!
            #self.secondWin.id1.emit(self.line1_val)
            #self.secondWin.id2.emit(self.line2_val)
        
        
        
        
        
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    ex = FirstWindow()
    
    sys.exit(app.exec_())