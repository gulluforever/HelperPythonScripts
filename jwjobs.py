from bs4 import BeautifulSoup
import requests
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import urllib.request
import os
import mimetypes
global pageurls
pageurls = []
def get_urls(url):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    r = requests.get(url,headers = user_agent)
    data = r.text
    soup = BeautifulSoup(data)
    div = soup.find('div', class_="panel-content")
    links = div.findAll('a')
    for a in links:
        try:
            if 'deccanchronicle.com' in a['href']:
                r = requests.get(a['href'],headers = user_agent)
                data = r.text
                soup = BeautifulSoup(data)
                title = soup.find('h1', class_="title")
                imgurl = soup.find('div',class_="field-item even")
                orgimgurl = imgurl['resource']
                data = data[data.index('<div class="field field-name-field-image'):]
                data = data[:data.index('<div class="field field-name-field-tags')]
                soup = BeautifulSoup(data)
                texts = soup.find_all('p')
                content = ""
                if(len(texts)==0):
                    raise
                for text in texts:
                    content = content+"<p>"+text.getText()
                content = content + "<p>" + a['href']
                post = WordPressPost()
                post.title = title.get_text() #Setting Post Title
                urllib.request.urlretrieve(orgimgurl, os.path.basename(orgimgurl))
                filename = os.path.basename(orgimgurl)
                data = {
                    'name': os.path.basename(orgimgurl),
                    'type': mimetypes.guess_type(filename)[0],  # mimetype
                    }
                with open(filename, 'rb') as img:
                    data['bits'] = xmlrpc_client.Binary(img.read())
                response = wp.call(media.UploadFile(data))
                attachment_id = response['id']
                post.thumbnail = attachment_id #Setting Feautured Image
                post.content = content #Setting Content Up
                post.terms_names = {
                    'post_tag': ['snews', 'andhrapradesh'], #Change Tags here
                    'category': ['State News'] #Change Category Here
                    }
                post.post_status = 'publish'
                wp.call(NewPost(post))
                #print ("Post Id is %s" %(wp.call(NewPost(post))))
                print("%s is Posted!" %(title.get_text()))
                #input("Press Enter to continue...")
        except:
            print('Some Error On This Post %s ' %(title.get_text()))
            pass
def pages20(mainurl):
    global pageurls
    pageurls.append(mainurl)
    for i in range(1,20):
        url = mainurl+"?page=%d" %(i)
        pageurls.append(url)
    pageurls.reverse()
    for pageurl in pageurls:
        get_urls(pageurl)
        print("%s in DONE!" %(pageurl))
wp = Client('http://seemandhra.co.in/xmlrpc.php', 'Seemandhra', 'Ter')
pages20("http://www.deccanchronicle.com/south/andhra-pradesh")
    
    
    
