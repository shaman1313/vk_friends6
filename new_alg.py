import urllib.request
import urllib.parse
from xml.dom.minidom import *
import sys
import os
import time

print ('Hello! I`m script for frends search')
start=time.time()
whoAmI='319299777'          #ID or short adress of first person
whoIsSome='19036902'       #ID or short adress of second person
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

firstP_id=isIdAndConvert(whoAmI)
print (firstP_id)
secondP_id=isIdAndConvert(whoIsSome)
print (secondP_id)

contact=''
connection_table=[]

listOfFr_1p_lay1=getListOfFriends(firstP_id)
print("In layer 1 are %d entries for P1" % len(listOfFr_1p_lay1))


print('Building the chains...')


mn_listOfFr_1p=set(listOfFr_1p_lay1)

if secondP_id in mn_listOfFr_1p:
    print ('Second person is your friend!')
    sys.exit()          ######## Exit if Match results
else:
    iteration=0
    for member in listOfFr_1p_lay1:
        member_friends=getListOfFriends(member)
        mn_member_friends=set(member_friends)
        iteration+=1
        sys.stdout.write("\rdone %.2f persent" % ((iteration/len(listOfFr_1p_lay1))*100))
        if secondP_id in mn_member_friends:
            ########## add chain ########
            chain=[firstP_id, member, secondP_id]
            connection_table.append(chain)

print('\n%d chains were build:' % len(connection_table))

finish=time.time()
exect=finish-start
print('On work %.3f seconds' % exect)
##############################################################################################
#second variant
#restart the timer
start=time.time()

contact=''


listOfFr_1p_lay1=getListOfFriends(firstP_id)
print("In layer 1 are %d entries for P1" % len(listOfFr_1p_lay1))
listOfFr_2p_lay1=getListOfFriends(secondP_id)
print("In layer 1 are %d entries for P2" % len(listOfFr_2p_lay1))

mn1=set(listOfFr_1p_lay1)   #Checking for mutual fr in layer1
mn2=set(listOfFr_2p_lay1)
mn_betw=mn1 & mn2
print ('You have %d mutual friends' % len(list(mn_betw)))
contact=list(mn_betw)
connection_table=[]


for member in contact:
    chain=[firstP_id, member, secondP_id]
    connection_table.append(chain)
    
print('\n%d chains were build:' % len(connection_table))
finish=time.time()
exect=finish-start
print('On work %.3f seconds' % exect)
print ('Generation the result file')
start=time.time()



########################################################################################
#           GENERATION THE HTML-FILE - result; and out the result to terminal
########################################################################################
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
f.close()

for mem in connection_table:
    f=open("result.html", 'a', encoding='utf-8')
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
    f.close()
    gi+=1
    sys.stdout.write('\n')

f=open("result.html", 'a', encoding='utf-8')
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























