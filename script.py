import urllib.request
import urllib.parse
from xml.dom.minidom import *
import sys
import os
import time

print ('Hello! I`m script for frends search')

whoAmI='319299777'          #ID or short adress of first person
whoIsSome='319299777dd'       #ID or short adress of second person
#alesbelarus
#manzhesova.marina
#199922935   kupchik
#319784945   banned
#529501        no user
#319299777 its me
#200323901   vasya dyachenko
#denis_lesko
#h.victory not friend but 2 mutual fr
#46773881       4 friends between




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
    if len(xml.getElementsByTagName('deactivated')) != 0:
        print ('User was banned or deleted acount')
        sys.exit()
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
        sys.exit()

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


#######################################################################   func user data
def getUserData(person_id):
    global info_lst
    info_lst=[]
    person=urllib.request.urlopen("https://api.vk.com/method/users.get.xml?user_id=%d&fields=photo_100,bdate" % int(person_id))
    dec_person=person.read().decode("utf-8")

    f=open("person.xml", 'w', encoding='utf-8')
    f.write(dec_person)
    f.close()

    xml=parse('person.xml')

    uid=xml.getElementsByTagName('uid')
    for node in uid:
        uid_v=(node.childNodes[0].nodeValue)
    info_lst.append(uid_v)

    first_name=xml.getElementsByTagName('first_name')
    for node in first_name:
        first_name_v=(node.childNodes[0].nodeValue)
    info_lst.append(first_name_v)

    if first_name_v=='DELETED':
        last_name_v='DELETED'
    else:
        last_name=xml.getElementsByTagName('last_name')
        for node in last_name:
            last_name_v=(node.childNodes[0].nodeValue)
        info_lst.append(last_name_v)
    
    first_name_v=first_name_v.replace('\u0456', 'i')
    first_name_v=first_name_v.replace('\u0406', 'I')
    last_name_v=last_name_v.replace('\u0456', 'i')
    last_name_v=last_name_v.replace('\u0406', 'I')

    bdate_v=''
    bdate=xml.getElementsByTagName('bdate')
    for node in bdate:
        bdate_v=(node.childNodes[0].nodeValue)
    if len(bdate_v) != 0:
        info_lst.append(bdate_v)
    else:
        info_lst.append(' ')

    photo_100=xml.getElementsByTagName('photo_100')
    for node in photo_100:
        photo_100_v=(node.childNodes[0].nodeValue)
    info_lst.append(photo_100_v)
    
    sys.stdout.write('%s %s' % (first_name_v, last_name_v))
    return info_lst
########################################################################
#################################################################################################################
#
#                   Block of code
#
#################################################################################################################
print('First user')
firstP_id=isIdAndConvert(whoAmI)
print('second user')
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
                finish=time.time()
                exect=finish-start
                print('On work %.3f seconds\n' % exect)
                
            else:
                print ('I`m don`t find any chains')

########################################################################################
#           GENERATION THE HTML-FILE - result; and out the result to terminal
########################################################################################



start=time.time()
gi=0
f=open("result.html", 'w', encoding='utf-8')
f.write('''<!DOCTYPE html >
<head>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta http-equiv="content-type" content="text/html; charset=utf-8">
<meta name="description" content="">
<title>Results</title>
  <link rel="stylesheet" type="text/css" href="result_files/fonts_cnt.css">
  <link rel="stylesheet" type="text/css" href="result_files/common.css">
  <link type="text/css" rel="stylesheet" href="result_files/docs.css">
  <style>
   TABLE {
	table-layout: fixed; /* Ячейки фиксированной ширины */
   }
   td {
	white-space: nowrap; /* Запрещаем перенос строк */
	overflow: hidden; /* Обрезаем все, что не помещается в область */
	text-overflow: ellipsis; /* Добавляем многоточие */
	
   }
  </style>
 </head>

<body>
  
  <div id="notifiers_wrap" class="fixed" style="bottom: 0px;"></div>
  <div class="scroll_fix_wrap _page_wrap" id="page_wrap" style="height: auto; margin-top: 0px;">
  <div>
  <div class="scroll_fix" style="width: 1902px;">
  

  <div id="page_header_cont" class="page_header_cont">
	<div class="back"></div>
	<div id="page_header_wrap" class="page_header_wrap" style="width: 1902px; margin-left: 0px;">
	  <a class="top_back_link" href="" id="top_back_link"  style="max-width: 1867px; display: none;"></a>
	  <div id="page_header" class="p_head p_head_l1" style="width: 960px">
		<div class="content">
		  <div id="top_nav" class="head_nav"></div>
		</div>
	  </div>
	</div>
  </div>

  <div id="page_layout" style="width: 960px;">
	<div id="side_bar" class="fl_l " style="">
	  
	</div>

	<div id="page_body" class="fl_r " style="width: 795px;">
	  <div id="header_wrap2">
		<div id="header_wrap1">
		  <div id="header" style="display: none">
			<h1 id="title">false</h1>
		  </div>
		</div>
	  </div>
	  <div id="wrap_between"></div>
	  <div id="wrap3"><div id="wrap2">
  <div id="wrap1">
  
  
  
  <div class="wide_column_wrap">
	<div class="wide_column" id="wide_column">
	  <div class="page_block">
  <h2 class="page_block_h2"><div class="page_block_header">
	<div id="docs_title" class="docs_title">Chains:</div>''')
f.close()
chains_number=len(connection_table)
f=open("result.html", 'a', encoding='utf-8')
f.write('''<div id="docs_summary" class="page_block_header_count">%d</div>
	
  </div></h2>
  
  <div class="docs_wrap">
	<div id="docs_list">''' % chains_number)
#f.close()

for mem in connection_table:
	#f=open("result.html", 'a', encoding='utf-8')
	f.write('''<div class="docs_item _docs_item" id="docs_file_319299777_414600186">
 <table width="100%" >
  <tr>''')

	one_chain=[]
	for user in connection_table[gi]:
		one_chain.append(getUserData(user))
		sys.stdout.write(' -> ')
	for mem in one_chain:
		f.write('''<td align="center">
	<img  src="%s" ></td>''' % mem[4])
	
	f.write('''</tr>
   
	<tr>''')
	for mem in one_chain:
		f.write('''<td align="center">
	<a class="docs_item_name" href="https://vk.com/id%s" >%s %s</a>
	<div class="docs_item_date">%s</div></td>''' % (mem[0], mem[1], mem[2], mem[3]))
	f.write('''</tr>
   
	</table>
  
	 </div>''')
	#f.close()
	gi+=1
	sys.stdout.write('\n')

#f=open("result.html", 'a', encoding='utf-8')
f.write('''</div>
 </div>
</body></html>''')
f.close()



#####################################################################################################
#### Clearing the working directory
os.remove('friends.xml')
os.remove('isUser.xml')
os.remove('person.xml')
finish=time.time()
exect=finish-start
print('On work %.3f seconds' % exect)























