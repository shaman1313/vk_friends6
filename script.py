import urllib.request
import urllib.parse
from xml.dom.minidom import *
import sys


print ('Hello! I`m script for frends search')

whoAmI='319299777'          #ID or short adress of first person
whoIsSome='alesbelarus'       #ID or short adress of second person
#alesbelarus
#manzhesova.marina
#199922935   kupchik
#319784945   banned
#529501        no user
#319299777 its me
#200323901   vasya dyachenko
#denis_lesko
#19036902 not friend but 2 mutual fr




#######################################################################################################
#
#               Defining of functions
#
#############################################################   function for convert short adress in ID
# This function include the error checking for unknown adress or ID
# Function return the string with ID

def isIdAndConvert (whoIs):

    resp=urllib.request.urlopen("https://api.vk.com/method/users.get.xml?user_ids=%s" % whoIs)
    dec_resp=resp.read().decode("utf-8")

    f=open("isUser.xml", 'w', encoding='utf-8')
    f.write(dec_resp)
    f.close()

    xml=parse('isUser.xml')
    
    if len(xml.getElementsByTagName('error_code')) == 0:
        print ("No err")
        id_idByName_request=xml.getElementsByTagName('uid')
        for node in id_idByName_request:
                id_whoIs=node.childNodes[0].nodeValue ######### ID of user!!!!!!
                print ("Ok... Profile ID is ", id_whoIs)
        return id_whoIs

    
    else:
        error_code=xml.getElementsByTagName('error_code')
        for node in error_code:
            error_code_is=node.childNodes[0].nodeValue
            print ("Err in code:", error_code_is)

        error_msg=xml.getElementsByTagName('error_msg')
        for node in error_msg:
            error_msg_is=node.childNodes[0].nodeValue
            print ("Err with msg:", error_msg_is)

#############################################################################################################

################################################################## Function for getting friendlist for user ID
# Function return the list with ID of user`s friends as members of list
def getListOfFriends (person_id):

    friendsOfP=urllib.request.urlopen("https://api.vk.com/method/friends.get.xml?user_id=%d" % int(person_id))
    dec_friendsOfP=friendsOfP.read().decode("utf-8")
    #print(dec_friendsOfP)
    f=open("friends.xml", 'w', encoding='utf-8')
    f.write(dec_friendsOfP)
    f.close()

    xml=parse('friends.xml')
    uid=xml.getElementsByTagName('uid')
    listOfFriends=[]  #list of friens
    for node in uid:
        listOfFriends.append(node.childNodes[0].nodeValue)
    #print("\n", listOfFriends_1P)
    return listOfFriends
###############################################################################################################

############################################################################ Function to form first half of chain

def searchMatchR(list1, list2, result, count):
    for a in list1:
        for b in list2:
            if a == b:
                result.append([])
                result[count].append(firstP_id)
                result[count].append(a)
                
                return 0
    return 1

########################################################################### Function to form second half of chain
def searchMatchR_2(list1, list2, result, count):
    for a in list1:
        for b in list2:
            if a == b:
                result[count].append(b)
                result[count].append(secondP_id)
                
                return 0
    return 1
#################################################################################################################
#################################################################################################################
#
#                   Block of code
#
#################################################################################################################

firstP_id=isIdAndConvert(whoAmI)
print (firstP_id)
secondP_id=isIdAndConvert(whoIsSome)
print (secondP_id)


listOfFr_1p_lay1=getListOfFriends(firstP_id)
print("In layer 1 are %d entries for P1" % len(listOfFr_1p_lay1))
mn1=set(listOfFr_1p_lay1)

if secondP_id in mn1:
    print ('Second Pers is your friend!')
    sys.exit()      ######## Exit if Match results
    
listOfFr_2p_lay1=getListOfFriends(secondP_id)
print("In layer 1 are %d entries for P2" % len(listOfFr_2p_lay1))

mn1=set(listOfFr_1p_lay1)   #Checking for mutual fr in layer1
mn2=set(listOfFr_2p_lay1)
mn_betw=mn1 & mn2

if len(list(mn_betw)) == 0:
    print('You haven`t mutual friends in 1st layer')###if you don`t have friends in L1
    print('Downloading info for layer2:')

    listOfFr_1p_lay2=[]##friendslist of L2 for P1
    i=0
    for ides in listOfFr_1p_lay1:
        listOfFr_1p_lay2.extend(getListOfFriends(ides))
        i+=1
        sys.stdout.write("\rdone %.2f persent" % (i/len(listOfFr_1p_lay1)*100))
    print("\nIn layer 2 are %d entries for P1" % len(listOfFr_1p_lay2))
    
    mn1_l2=set(listOfFr_1p_lay2)
    mn_betw21=mn1_l2 & mn2#### the difference between L2P1 and L1P2
    if len(list(mn_betw21)) == 0:
        #print('You haven`t mutual friends in 2nd layer')
        listOfFr_2p_lay2=[]
        i=0
        for ides in listOfFr_2p_lay1:
            listOfFr_2p_lay2.extend(getListOfFriends(ides))
            i+=1
            sys.stdout.write("\rdone %.2f persent" % (i/len(listOfFr_2p_lay1)*100))
        print("\nIn layer 2 are %d entries" % len(listOfFr_2p_lay2))

        mn2_l2=set(listOfFr_2p_lay2)
        mn_betw22=mn1_l2 & mn2_l2######the difference between L2P1 and L2P2
        if len(list(mn_betw22)) == 0:
            print('You haven`t mutual friends in 2st layer')
        else:
            print ('You have %d mutual friends' % len(list(mn_betw22)))
            #print (list(mn_betw22))
            #sys.exit()          ######## Exit if Match results
    
                
    else:
        print ('You have %d mutual friends' % len(list(mn_betw21)))
        #print (list(mn_betw21))
        sys.exit()          ######## Exit if Match results

else:
    print ('You have %d mutual friends' % len(list(mn_betw)))
    #print (list(mn_betw))
    sys.exit()          ######## Exit if Match results
##################################################################################################################
print('Building the chains...')
contact=list(mn_betw22)
connection_table=[]
count=0
jj=0
for mem in contact:
    cont_frlst=getListOfFriends (mem)
    suc_f=searchMatchR(cont_frlst, listOfFr_1p_lay1, connection_table, count)
    if suc_f==0:
        connection_table[count].append(mem)
        searchMatchR_2(cont_frlst, listOfFr_2p_lay1, connection_table, count)
        count+=1
        continue
    jj+=1
    sys.stdout.write("\rdone %.2f persent" % ((jj/len(contact))*100))

#############################################################

print ('\n')

#######################################################################func user data
def getUserData(person_id):

    person=urllib.request.urlopen("https://api.vk.com/method/users.get.xml?user_id=%d" % int(person_id))
    dec_person=person.read().decode("utf-8")

    f=open("person.xml", 'w', encoding='utf-8')
    f.write(dec_person)
    f.close()

    xml=parse('person.xml')
    uid=xml.getElementsByTagName('uid')
    for node in uid:
        uid_v=(node.childNodes[0].nodeValue)
    first_name=xml.getElementsByTagName('first_name')
    for node in first_name:
        first_name_v=(node.childNodes[0].nodeValue)
    last_name=xml.getElementsByTagName('last_name')
    for node in last_name:
        last_name_v=(node.childNodes[0].nodeValue)

    first_name_v=first_name_v.replace('\u0456', 'i')
    last_name_v=last_name_v.replace('\u0456', 'i')
    
    sys.stdout.write('%s %s' % (first_name_v, last_name_v))
    return 0
########################################################################
gi=0
for mem in connection_table:
    
    for user in connection_table[gi]:
        getUserData(user)
        sys.stdout.write(' -> ')
    gi+=1
    sys.stdout.write('\n')














