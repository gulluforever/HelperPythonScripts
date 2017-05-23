import re,requests
# -*- coding: utf-8 -*-
import urllib,mimetypes,os,htmlentitydefs
from bs4 import BeautifulSoup
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
pageurls = []

def scrapedeals(url):
    try:
        print 'Going With %s' %(url)
        dealspagesource = requests.get(url).text
        soup = BeautifulSoup(dealspagesource)
        boxes = soup.find_all('div',class_='box')
        for box in boxes:
            try:
                dealurlfind = box.find('a',id=re.compile('A_*'))
                dealurl = dealurlfind['href']
                dealtitle = dealurlfind['title']
                dealtitle = dealtitle.replace('snapdeal','')
                dealtitle = dealtitle.replace('Snapdeal','')
                #dealtitle = unescape(dealtitle)
                dealshopurl = box.find('a',id='shop_now')['href'].replace('http://dealschintu.com/url.php?url=','')
                if '&uid=' in dealshopurl:
                    dealshopurl = dealshopurl[:dealshopurl.index('&uid=')]
                #print dealshopurl
                #print dealtitle
                #print dealurl
                originalprice = box.find('div',id='DIV_12').text.lstrip().rstrip()
                discountprice = box.find('div',id='DIV_13').text.lstrip().rstrip()
                #print originalprice.lstrip().rstrip()
                #print discountprice.lstrip().rstrip()
                #print 'Got Box Details'
                if 'threads' in dealurl:
                    post = WordPressPost()
                    dealurlsource = requests.get(dealurl).text
                    print 'Loaded Deal Url'
                    dealsoup = BeautifulSoup(dealurlsource)
                    article = dealsoup.find('div',class_="messageContent")
                    article = str(article).replace('<br/>','')
                    #print article
                    imgurlnode = dealsoup.find('img',class_="bbCodeImage LbImage")['src']
                    #print imgurlnode
                    urllib.urlretrieve(imgurlnode,os.path.basename(imgurlnode))
                    filename = os.path.basename(imgurlnode)
                    data = {
                        'name' : os.path.basename(imgurlnode),
                        'type': mimetypes.guess_type(filename)[0],
                        }
                    with open(filename, 'rb') as img:
                        data['bits'] = xmlrpc_client.Binary(img.read())
                    response = wp.call(media.UploadFile(data))
                    #print response
                    attachmenturl = response['url']
                    #print attachmenturl
                    attachment_id = response['id']
                    post.thumbnail = attachment_id #Setting Feautured Image
                    post.terms_names = {
                                'category': ['SnapDeal'] #Change Category Here
                                }
                    post.title = dealtitle
                    post.custom_fields = []
                    post.custom_fields.append({
                        'key' : 'disable_parts',
                        'value' : 0})
                    post.custom_fields.append({
                        'key' : 'filter_featured_for',
                        'value' : 'featured_for_slider'})
                    post.custom_fields.append({
                        'key' : 'is_editor_choice',
                        'value' : 0})
                    post.custom_fields.append({
                        'key' : 'is_featured',
                        'value' : 0})
                    post.custom_fields.append({
                        'key' : 'meta_data_filter_cat',
                        'value' : -1})
                    post.custom_fields.append({
                        'key' : 'post_size',
                        'value' : 'normal_post'})
                    post.custom_fields.append({
                        'key' : 'rehub_framework_post_type',
                        'value' : 'regular'})
                    post.custom_fields.append({
                        'key' : 'rehub_main_product_price',
                        'value' : originalprice })
                    post.custom_fields.append({
                        'key' : 'rehub_offer_btn_text',
                        'value' : 'Check Latest Price'})
                    post.custom_fields.append({
                        'key' : 'rehub_offer_logo_url',
                        'value' : 'http://couponsmama.in/wp-content/uploads/2015/08/snapdealbrand.jpg'})
                    post.custom_fields.append({
                        'key' : 'rehub_offer_name',
                        'value' : dealtitle})
                    post.custom_fields.append({
                        'key' : 'rehub_offer_product_desc',
                        'value' : dealtitle})
                    post.custom_fields.append({
                        'key' : 'rehub_offer_product_price',
                        'value' : discountprice})
                    post.custom_fields.append({
                        'key' : 'rehub_offer_product_price_old',
                        'value' : originalprice})
                    post.custom_fields.append({
                        'key' : 'show_featured_image',
                        'value' : 1})
                    post.custom_fields.append({
                        'key' : 'rehub_offer_product_thumb',
                        'value' : attachmenturl})
                    post.custom_fields.append({
                        'key' : 'rehub_offer_product_url',
                        'value' : dealshopurl})
                    post.custom_fields.append({
                        'key' : 'rehub_post_side[show_featured_image]',
                        'value' : 0})
                    content = article.replace(imgurlnode,attachmenturl)
                    content = remove_img_tags(content)
                    #content = unescape(content)
                    post.content = content
                    post.post_status = 'publish'
                    wp.call(NewPost(post))
                    print 'Posted at %s' %(dealtitle)
                #raw_input()
            except:
                print 'Error at %s' %(dealtitle)
                pass
        #print 'Completed Page %s' %(url)
    except:
        pass



def remove_img_tags(data):
    p = re.compile(r'<img.*?/>')
    return p.sub('', data)

def createdealpages():
    global pageurls
    url = "http://dealschintu.com/pages/homepage/?pn=67&cat=901"
    for i in range(1,16):
        url = "http://dealschintu.com/pages/homepage/?pn="+str(i)+"&cat=903"
        pageurls.append(url)
    pageurls.reverse()
    for pageurl in pageurls:
        scrapedeals(pageurl)
        print("%s in DONE!" %(pageurl))
wp = Client('http://couponsmama.in/xmlrpc.php', 'admin', 'gesdfsdfs3.')
createdealpages()
