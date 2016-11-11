import sys

sys.path.append(".\\modules")
from window import *
from script import *

if __name__=="__main__":
    if len (sys.argv) == 1:
        print ("Use friends with parameters.\nIf you want run the program in graphical mode type 'friends.py -g' \
         \nFor console mode type 'friends.py [first ID] [second ID]', \n\twhere first ID and second ID - the IDes or short adress of VK users")
        sys.exit (1)
        

    if len (sys.argv) == 2:
        if sys.argv[1]=='-g':
            print ("Start GUI, wait")
            GUI()
        else:
            print ('Unknown arguments\n')
            print ("Use friends with parameters.\nIf you want run the program in graphical mode type 'friends.py -g'\nFor console mode type 'friends.py [first ID] [second ID]', \n\twhere first ID and second ID - the IDes or short adress of VK users")
            sys.exit (1)

    if len (sys.argv) > 3:
        print ("Error. Too many arguments")
        print ("Use friends with parameters.\nIf you want run the program in graphical mode type 'friends.py -g'\nFor console mode type 'friends.py [first ID] [second ID]', \n\twhere first ID and second ID - the IDes or short adress of VK users")
        sys.exit (1)
    if len(sys.argv)==3:
        first = sys.argv[1]
        second = sys.argv[2]
        main(first, second)

    