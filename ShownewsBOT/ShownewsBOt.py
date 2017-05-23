import re,requests,string,random,threading,os,inspect,gc,pdb,urllib2,urllib
from itertools import cycle
def load(filename):
    with open(filename) as f:
        return [line.rstrip() for line in f]
def checklink(curl,lsi):
    try:
        global ctot
        murl=curl.replace("Comment","Shownews")
        thepage2=requests.get(murl,timeout=tout)
        if lsi in thepage2.text:
            print"Posted to Site : " + str(murl) + "Urls lefts: " +str(len(urls))
            ctot = ctot + 1
            slist = open('res\output.txt', 'a+')
            slist.write("\n" +murl)
            slist.close()

    except:
        pass

def postcomment():
    while len(urls)>0 :
        try:
            #global x,y,z
            curl = urls.pop(0).replace("Shownews","Comment")
            #print "working on " + str(curl.replace("Comment","Shownews"))
            readcomment = open(os.getcwd()+"\\comments\\"+ctnames.next(),'r')
            comment = readcomment.read()
            lsi = lsis.next()
            payload = {'com_name':lsi, 'com_content':comment,'B1':""}
            thepage1 = requests.post(curl,payload,timeout=tout)
            #print "Posted now Checking link"
            checklink(curl,lsi)
        except:
            pass

#Main PROGRAM
urls = load('res\urls.txt')
lsis = cycle(load('res\lsi.txt'))
tarray,cfnames=[],[]
for filename in os.listdir("comments"):
        cfnames.append(filename)
ctot,cmod = 0,0
ctnames =cycle(cfnames)
print "~~~~~~~~~~~~~~~~~~~~ShowNews COMMENTOR BOT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ "
totallinks = len(urls)
print "No of the Urls "+str(len(urls))
noofthreads = input("Enter the Number of Threads : ")
tout = input("Enter Timeout : ")
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
