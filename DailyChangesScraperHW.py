import requests,threading
from datetime import datetime
from datetime import timedelta
from bs4 import BeautifulSoup
def logic():
    try:
        global ctot
        curl = urls.pop(0)
        print "Working on Url : " +curl
        queueLock = threading.Lock()
        stext = requests.get(curl).text
        index = stext.index("deleted-domains-tab")
        soup = BeautifulSoup(stext[index:])
        tds = []
        tds = soup.find_all("td")
        for td in tds:
            slist.write("\n"+td.get_text())
            ctot = ctot+1
    except:
        raise
    finally:
        if len(urls)>0:
            logic()
print "Daily Changes Scraper BOT"
print "Date Formate Should be YYYY-MM-DD"
from1 = raw_input("Enter the Starting Date : ")
to1 = raw_input("Enter the Ending Date: ")
date_format = "%Y-%m-%d"
d0 = datetime.strptime(from1,date_format)
d1 = datetime.strptime(to1,date_format)
delta = d1 - d0
noofthreads = input("Enter the Number of Threads : ")
#enterminpr = raw_input("Enter the Minimum PR :")
nameoutput = raw_input("Enter the name of the Output File (with .txt extension): ")
slist = open(nameoutput, 'a+')
ctot = 0
urls = []
tarray = []
for nurls in range(0,delta.days+1):
    date = str(d0+timedelta(days=nurls)).split()
    geturl = "http://www.dailychanges.com/hostwindsdns.com/"+str(date[0])+"/"
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
print "File Closed For Writing"
print "Total Domains : " + str(ctot)
