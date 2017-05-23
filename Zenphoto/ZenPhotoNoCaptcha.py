import re,requests,string,random,threading,os,inspect,gc,pdb,urllib2,urllib
from itertools import cycle
from bs4 import BeautifulSoup
def load(filename):
    with open(filename) as f:
        return [line.rstrip() for line in f]


def postcomment():
    
    while len(urls)>0 :
        
        try:
            global ctot
            #global x,y,z
            curl = urls.pop(0)
            #print ctnames.next()
            readcomment = open(os.getcwd()+"\\comments\\"+ctnames.next(),'r')
            comment = readcomment.read()
            #print comment
            readcomment.close()
            emailt = ''.join((random.choice(string.ascii_lowercase+string.ascii_uppercase) for _ in xrange(random.randint(5,15)))) + "@gmail.com"
            print "Trying to Post on "+str(curl)
            www1 = wwws.next()
            payload = {'comment':'1','remember':'0','name':lsis.next(),'email':emailt,'website':www1,'comment':comment}
            thepage2 = requests.post(curl,payload,timeout=tout).text
            if str(www1)in thepage2:
                print "Posted on Site : " + curl + " Urls Remaining : " + str(len(urls))
                ctot = ctot + 1
                print "Total POSTED : " + str(ctot)
                slist = open('res\output.txt', 'a+')
                slist.write("\n" +curl)
                slist.close()
        except:
            global clear
            clear = clear + 1
            if clear>100:
                clear = 0
                os.system("cls")
            os.system("cls")
            raise
        
#Main PROGRAM
urls = load('res\urls.txt')
lsis = cycle(load('res\lsi.txt'))
wwws = cycle(load('res\www.txt'))
tarray,success,cfnames=[],[],[]
for filename in os.listdir("comments"):
        cfnames.append(filename)
clear,ctot,cmod = 0,0,0
ctnames =cycle(cfnames)
print "~~~~~~~~~~~~~~~~~~~~WORDPRESS COMMENTOR BOT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "
totallinks = len(urls)
print "No of the Urls "+str(len(urls))
noofthreads = input("Enter the Number of Threads : ")
tout = input("Enter TimeOut Value : ")
if (totallinks<noofthreads) :
    noofthreads = totallinks
if totallinks>0 :
    for xd in range(0,noofthreads):
        t = threading.Thread(target=postcomment)
        t.daemon = True
        t.start()
        tarray.append(t)
for t in tarray:
    t.join()
#slist.close()
print "Program Completed Its Execution"
raw_input("Press ENTER to Exit the Program")
