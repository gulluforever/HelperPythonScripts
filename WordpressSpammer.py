import re,requests,string,random,threading,os,inspect,gc,pdb,urllib2,urllib
from itertools import cycle
from bs4 import BeautifulSoup
def load(filename):
    with open(filename) as f:
        return [line.rstrip() for line in f]
def postcomment(clink,cid,www1,lsi,item,bdftext):
    try:
        global ctot,cmod,slist
        #print ctnames.next()
        readcomment = open(os.getcwd()+"\\comments\\"+ctnames.next(),'r')
        comment = readcomment.read()
        #print comment
        readcomment.close()
        emailt = ''.join((random.choice(string.ascii_lowercase+string.ascii_uppercase) for _ in xrange(random.randint(5,15)))) + "@gmail.com"
        #print "Trying to Post on "+str(item)+" using LSI keyword "+str(lsi)+" and url with " +str(www1)
        payload = {'author':str(lsi), 'email':emailt, 'url':www1, 'comment':str(comment), 'submit':str(bdftext),'comment_post_ID':str(cid),'comment_parent':'0'}
        thepage2 = requests.post(clink,payload).text
        if str(www1)in thepage2:
            if "moderation" in thepage2 :
                #print "Moderation on Site : " +item
                cmod = cmod +1
                os.system('cls') #on windows
            else :
                print "Posted on Site : " +item
                ctot = ctot + 1
                slist = open('res\output.txt', 'a+')
                slist.write("\n" +item)
                slist.close()
    except:
        pass

def getsession():
    while len(urls)>0 :
        try:
            #global x,y,z
            curl = urls.pop(0)
            
            thepage1 = requests.get(curl).text
            
            clink = re.search("http:\/\/.*wp-comments-post\.php",thepage1).group(0)
            if "wp-comments-post" in clink:
                print "Working on " +str(curl)
                bdftext =""
                if "Post Comment" in thepage1:  bdftext = "Post Comment"
                elif "Submit Comment" in thepage1: bdftext = "Submit Comment"
                else :  bdftext = "Submit"
                if "shortlink" in thepage1:
                    temp = re.search("shortlink.*",thepage1).group(0)
                    cid = temp[temp.rfind("=")+1:temp.rfind('"')]
                    #print cid
                elif "canonical"in thepage1:
                    temp = re.search("canonical.*",thepage1).group(0)
                    cid = temp[temp.rfind("=")+1:temp.rfind('"')]
                    #print cid
            #if z > len(cfnames) : z = 0
            
            postcomment(clink,cid,wwws.next(),lsis.next(),curl,bdftext)
        except:
            pass
        
#Main PROGRAM
urls = load('res\urls.txt')
lsis = cycle(load('res\lsi.txt'))
wwws = cycle(load('res\www.txt'))
tarray,success,cfnames=[],[],[]
for filename in os.listdir("comments"):
        cfnames.append(filename)
x,y,z,ctot,cmod = 0,0,0,0,0
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
        t = threading.Thread(target=getsession)
        t.daemon = True
        t.start()
        tarray.append(t)
for t in tarray:
    t.join()
#slist.close()
print "Program Completed Its Execution"
raw_input("Press ENTER to Exit the Program")
