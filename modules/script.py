import sys
import os
import time
sys.path.append(".\\modules")
from function import *
from window import *

from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication, QLabel, QHBoxLayout, QVBoxLayout)



def main(first, second):
    print ('Hello! I`m script for frends search')

    whoAmI=first          #ID or short adress of first person
    whoIsSome=second       #ID or short adress of second person

    f=open("isUser.xml", 'w', encoding='utf-8')
    f.close()
    f=open("friends.xml", 'w', encoding='utf-8')
    f.close()
    f=open("person.xml", 'w', encoding='utf-8')
    f.close()

    print('First user')
    firstP_id=isIdAndConvert(whoAmI)
    print('second user')
    secondP_id=isIdAndConvert(whoIsSome)
    if firstP_id == secondP_id:
        print ('Error! The IDs are the same!')
        sys.exit()
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

        else:   #if you do not have mutual friends in layer 1
            print('Downloading info for layer2 (person 1):')

            listOfFr_1p_lay2=[]##friendslist of L2 for P1
            i=0     #iterator for progress indication
            for member in listOfFr_1p_lay1:#for each ID 
                listOfFr_1p_lay2.extend(getListOfFriends(member))
                i+=1
                sys.stdout.write("\rdone %.2f persent" % (i/len(listOfFr_1p_lay1)*100))
                
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

            else:
                print('Downloading info for layer2 (person 2):')
                listOfFr_2p_lay2=[]
                i=0
                for member in listOfFr_2p_lay1:#for each ID 
                    listOfFr_2p_lay2.extend(getListOfFriends(member))
                    i+=1
                    sys.stdout.write("\rdone %.2f persent" % (i/len(listOfFr_2p_lay1)*100))
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
                    
                else:
                    print ('I`m don`t find any chains')
                    exiter()
                    sys.exit()

    result(connection_table)
    exiter()