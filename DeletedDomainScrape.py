import requests,threading
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
def logic():
    try:
        global ctot
        curl = urls.pop(0)
        print ("Working on Url : " +curl);
        queueLock = threading.Lock()
        stext = requests.get(curl).text
        soup = BeautifulSoup(stext)
        tds = []
        tds = soup.find_all("td")
        if tds[1246].get_text() >= enterminpr:
            aurl =  str(curl[0:-6] + str(int(curl[-6])+1)+".html")
            #print aurl
            urls.append(aurl)
        domainname = []
        for r in range(0,250):
            domainname.append(5*r)
        for dname in domainname:
            if tds[dname+1].get_text() >= enterminpr:
                #item = str(tds[dname].get_text()) +','+ str(tds[dname+1].get_text())
                item = str(tds[dname].get_text())
                #item = str(tds[dname].get_text())
                slist.write("\n" + item)
                ctot = ctot + 1
        
    except:
        raise                             
    finally:
        if len(urls)>0:
            logic()
print ("Deleted Domain Scraper BOT");
print ("Date Formate Should be YYYY-MM-DD");
from1 = input("Enter the Starting Date : ")
to1 = input("Enter the Ending Date: ")
date_format = "%Y-%m-%d"
d0 = datetime.strptime(from1,date_format)
d1 = datetime.strptime(to1,date_format)
delta = d1 - d0
noofthreads = int(input("Enter the Number of Threads : "))
enterminpr = input("Enter the Minimum PR :")
nameoutput = input("Enter the name of the Output File (with .txt extension): ")
slist = open(nameoutput, 'a+')
ctot = 0
urls = []
tarray = []
for nurls in range(0,delta.days+1):
    date = str(d0+timedelta(days=nurls)).split()
    geturl = "http://www.deleted-domain-list.com/domains-"+str(date[0])+"-sort-pagerank-1.html"
    urls.append(geturl)
#print urls
for xd in range(0,noofthreads):
        t = threading.Thread(target=logic)
        t.daemon = True
        t.start()
        tarray.append(t)
for t in tarray:
    t.join()

slist.close()
print ("File Closed For Writing");
print ("Total Domains : " + str(ctot));
