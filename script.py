import urllib.request
import urllib.parse
from xml.dom.minidom import *
import sys


print ('Hello! I`m script for frends search')

whoAmI='alesbelarus'
whoIsSome='manzhesova.marina'
#alesbelarus
#manzhesova.marina
#199922935   kupchik
#319784945   banned
#529501        no user
#319299777 its me


#############################################################   функция для конвертации короткого имени в uid
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
firstP_id=isIdAndConvert(whoAmI)
print (firstP_id)
secondP_id=isIdAndConvert(whoIsSome)
print (secondP_id)

############################################################################ функция получения списка друзей
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

listOfFr_1p_lay1=getListOfFriends(firstP_id)
print("In layer 1 are %d entries" % len(listOfFr_1p_lay1))
listOfFr_1p_lay2=[]
i=0
for ides in listOfFr_1p_lay1:
    listOfFr_1p_lay2.extend(getListOfFriends(ides))
    i+=1
    sys.stdout.write("\rdone %.2f persent" % (i/len(listOfFr_1p_lay1)*100))
print("\nIn layer 2 are %d entries" % len(listOfFr_1p_lay2))


listOfFr_1p_lay3=[]
i=0
for ides in listOfFr_1p_lay2:
    listOfFr_1p_lay3.extend(getListOfFriends(ides))
    i+=1
    sys.stdout.write("\rdone %.2f persent" % (i/len(listOfFr_1p_lay2)*100))
print("\nIn layer 3 are %d entries" % len(listOfFr_1p_lay2))
#print (listOfFr_1p_lay2)




#listOfFr_2p_lay1=getListOfFriends(secondP_id)




