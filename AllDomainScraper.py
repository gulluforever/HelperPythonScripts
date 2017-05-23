import requests,threading
from bs4 import BeautifulSoup
def logic():
    try:
        global ctot
        curl = urls.pop(0)
        print "Working on Url : " +curl
        queueLock = threading.Lock()
        stext = requests.get(curl).text
        soup = BeautifulSoup(stext)
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
url = raw_input("Enter URL : ")
nameoutput = raw_input("Enter the name of the Output File (with .txt extension): ")
noofthreads = input("Enter the Number of Threads : ")
lastpage = input("Enter Last Page: ")
ctot = 0
slist = open(nameoutput, 'a+')
urls =[]
tarray = []
for x in range(1,lastpage+1):
    urls.append(url[0:-6]+str(x)+".html")
#print urls
for xd in range(0,noofthreads):
        t = threading.Thread(target=logic)
        t.daemon = True
        t.start()
        tarray.append(t)
for t in tarray:
    t.join()
print "File Closed For Writing"
print "Total Domains : " + str(ctot)
