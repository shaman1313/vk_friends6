import urllib.request
import urllib.parse
from xml.dom.minidom import *

print ('Hello! I`m script for frends search')

whoAmI='319299777'
whoIsSome='manzhesova.marina'
#alesbelarus
#manzhesova.marina
#199922935   kupchik
#319784945   banned
#529501        no user
#319299777 its me


#############################################################   функция для конвертации ссылки в АйДи
def isIdAndConvert (whoIs):

    resp=urllib.request.urlopen("https://api.vk.com/method/friends.get.xml?user_ids=%s" % whoIs)
    dec_resp=resp.read().decode("utf-8")

    f=open("iserror.xml", 'w', encoding='utf-8')
    f.write(dec_resp)
    f.close()

    xml=parse('iserror.xml')

    if len(xml.getElementsByTagName('error_code')) == 0:
        print ("No err")
        return whoIs
    else:
        error_code=xml.getElementsByTagName('error_code')
        for node in error_code:
            error_code_is=node.childNodes[0].nodeValue
            print ("Err in code ", error_code_is)

        if error_code_is == '113':
            print ("Неверный идентификатор пользователя. Конвертирую...")
            idByName_request=urllib.request.urlopen("https://api.vk.com/method/utils.resolveScreenName.xml?screen_name=%s" % whoIs)
            dec_idByName_request=idByName_request.read().decode("utf-8")
            f=open("idByName.xml", 'w', encoding='utf-8')
            f.write(dec_idByName_request)
            f.close()

            xml=parse('idByName.xml')
            id_idByName_request=xml.getElementsByTagName('object_id')

            for node in id_idByName_request:
                id_whoIsSome=node.childNodes[0].nodeValue ######### ID of user!!!!!!
                print ("Ok... Profile ID is ", id_whoIsSome)
                return id_whoIsSome
                
#############################################################################################################
#firstP=isIdAndConvert(whoAmI)
firstP=int(str(whoAmI))
secondP=isIdAndConvert(whoIsSome)
print (firstP)

friendsOfFirstP=urllib.request.urlopen("https://api.vk.com/method/friends.get.xml?user_id=%d" % firstP)
dec_friendsOfFirstP=friendsOfFirstP.read().decode("utf-8")
print(dec_friendsOfFirstP)
f=open("firstP_ID.xml", 'w', encoding='utf-8')
f.write(dec_friendsOfFirstP)
f.close()
'''
xml=parse('iserror.xml')
error_code=xml.getElementsByTagName('error_code')
        for node in error_code:
            error_code_is=node.childNodes[0].nodeValue
            print ("Err in code ", error_code_is)
'''





