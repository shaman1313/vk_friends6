# vk_friends6
for search friends between two people in vk.com
Эта программа найдет цепочки из друзей между вами и любым другим пользователем vk.com - самой крупной социальной сети СНГ.

Возможности:

*Глубина поискового алгоритма - 5 (Искомый пользователь 5-й от вас в цепи)
*Алгоритм предлагает несколько вариантов цепочек
*Работа из командной строки и с помощью графического интерфейса
*Результат работы выводится в консоль, а также формируется результирующий html отчет
*не требует регистрации на сервисе vk.com, все что нужно - пара айди (или коротких адресов) двух пользователей

Требования:

*Установка Python3 (urllib, xml.dom.minidom)
*Установка PyQt5
*на ОС Linux - права записи в директории со скриптом

Для работы - запустить скрипт friends.py с параметрами "-g" для графического режима
                                                        "[ID1] [ID2]" - для текстового, где ID1
                                                        и ID2 - айди или короткие адреса пользователей вконтакте
########################################################################################################################
This program will be a chain of friends between you and any other user vk.com - the largest social network of the CIS.

Capabilities:

* The depth of the search algorithm - 5 (Seeking user is 5th from you in the chain)
* Algorithm offers several options chains
* Working from the command line and graphical user interface
* The output is displayed in the console, as well as forming the resulting html report
* Requires no registration vk.com service, all you need - a couple IDs (or short addresses) of the two users

Requirements:

* Install Python3 (urllib, xml.dom.minidom)
* Install PyQt5
* To Linux - write access to a directory with the script

For work - friends.py run the script with "-g" parameters for the graphics mode
                                                         "[ID1] [ID2]" - for the text mode, where ID1
                                                         and ID2 - ID or short address of VK users
