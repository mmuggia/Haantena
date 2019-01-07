import time
from bs4 import BeautifulSoup
import urllib
from urllib.request import Request, urlopen
from lxml import html
import requests
import nltk
import collections
import sqlite3 as sql

from types import *


#Settings
global write_sql
write_sql = True


    

"""

Pull words lists


"""


def negative_pull():
    list_negative = []
    print("negative - work")
    filename = 'gal_nega_words.txt' 
    File = open(filename,'r',encoding="utf8")
    for word in File:
        word = word[:-1]
        list_negative.append(word)
    return list_negative

def positive_pull():
    list_positive = []
    print("positive - work")
    filename = 'posi_words_he_3.txt' 
    File = open(filename,'r',encoding="utf8")
    for word in File:
        word = word[:-1]
        list_positive.append(word)
    #print(list_positive)
    return list_positive

list_negative = negative_pull()
list_positive = positive_pull()

"""

Get the links

"""


def get_ynet_links():
    
    ynet_link_list = []
    ynet_clean_list = []
    ynet_clean_list_2 = []

    req = Request("http://www.ynet.co.il/home/0,7340,L-2,00.html", headers={'User-Agent': 'Mozilla/5.0'})
    s = urlopen(req).read()
    soup = BeautifulSoup(s, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        ynet_link_list.append(href)


    ynet_artc_word = "/articles"
    ynet_starter = "http://www.ynet.co.il"
    for link in ynet_link_list:
        if link and ynet_artc_word in link:
            ynet_clean_list.append(link)

    for link in ynet_clean_list:
        if link and ynet_starter not in link:
            link = ynet_starter + link
            ynet_clean_list_2.append(link)

    return ynet_clean_list_2
#print(get_ynet_links())



def get_israel_ha_links():
    
    israel_ha_link_list = []
    israel_ha_clean_list = []
    israel_ha_clean_list_2 = []

    with urllib.request.urlopen("http://www.israelhayom.co.il/news") as url:
        s = url.read()

    soup = BeautifulSoup(s, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        israel_ha_link_list.append(href)

    israel_ha_artc_word = "/article"
    israel_ha_starter = "http://www.israelhayom.co.il"
    for link in israel_ha_link_list:
        if link and israel_ha_artc_word in link:
            israel_ha_clean_list.append(link)

    for link in israel_ha_clean_list:
        if link and israel_ha_starter not in link:
            link = israel_ha_starter + link
            israel_ha_clean_list_2.append(link)

    return israel_ha_clean_list_2
#print(get_israel_ha_links())


def get_mako_links():
    
    mako_link_list = []
    mako_clean_list = []
    mako_clean_list_2 = []

    with urllib.request.urlopen("http://www.mako.co.il/news?partner=NavBar") as url:
        s = url.read()

    soup = BeautifulSoup(s, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        mako_link_list.append(href)

    mako_artc_word = "/news-"
    mako_starter = "http://www.mako.co.il"
    for link in mako_link_list:
        if link and mako_artc_word in link:
            mako_clean_list.append(link)

    for link in mako_clean_list:
        if link and mako_starter not in link:
            link = mako_starter + link
            mako_clean_list_2.append(link)

    return mako_clean_list_2
#print(get_mako_links())


def get_walla_links():
    
    walla_link_list = []
    walla_clean_list = []
    walla_clean_list_2 = []

    with urllib.request.urlopen("https://news.walla.co.il") as url:
        s = url.read()

    soup = BeautifulSoup(s, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        walla_link_list.append(href)

    #print(soup.prettify())


    walla_artc_word = "/item"
    walla_starter = "https://news.walla.co.il/"
    for link in walla_link_list:
        if link and walla_artc_word in link:
            walla_clean_list.append(link)
    #del walla_clean_list[-2:-1]

    for link in walla_clean_list:
        if link and walla_starter not in link:
            link = walla_starter + link
            walla_clean_list_2.append(link)

    return walla_clean_list_2
#print(get_walla_links())


def get_calcal_links():
    
    calcal_link_list = []
    calcal_clean_list = []
    calcal_clean_list_2 = []

    with urllib.request.urlopen("https://www.calcalist.co.il/home/0,7340,L-8,00.html") as url:
        s = url.read()

    soup = BeautifulSoup(s, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        calcal_link_list.append(href)

    calcal_artc_word = "/articles"
    calcal_starter = "https://www.calcalist.co.il"
    unwanted_word = "https://xnet.ynet.co.il"
    
    for link in calcal_link_list:
        if link and calcal_artc_word in link:
            calcal_clean_list.append(link)
            
    for link in calcal_clean_list:
        if link and calcal_starter not in link:
            link = calcal_starter + link
            calcal_clean_list_2.append(link)
            
    dood = set([x for x in calcal_clean_list_2 if calcal_clean_list_2.count(x) > 1])
    calcal_clean_list_2 = list(set(calcal_clean_list_2) - set(dood))
    for link in dood:
        calcal_clean_list_2.append(link)
        
    for link in calcal_clean_list_2:
        if unwanted_word in link:
            calcal_clean_list_2.remove(link)

    return calcal_clean_list_2
#print(get_calcal_links())


def get_maariv_links():
    
    maariv_link_list = []
    maariv_clean_list = []

    with urllib.request.urlopen("http://www.maariv.co.il/news") as url:
        s = url.read()

    soup = BeautifulSoup(s, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        maariv_link_list.append(href)
    


    maariv_artc_word = "/Article"
    maariv_starter = "http://www.maariv.co.il"
    for link in maariv_link_list:
        if link and maariv_artc_word in link:
            maariv_clean_list.append(link)
    for link in maariv_clean_list:
        if link and "http" in link:
            maariv_clean_list.remove(link)
    maariv_clean_list.pop(-1)
    return(maariv_clean_list)
#print(get_maariv_links())



def get_kikar_links():
    
    kikar_link_list = []
    kikar_clean_list = []
    kikar_clean_list_2 = []

    with urllib.request.urlopen("http://www.kikar.co.il/news") as url:
        s = url.read()

    soup = BeautifulSoup(s, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        kikar_link_list.append(href)

    #print(soup.prettify())


    kikar_artc_word = "/articles"
    kikar_starter = "http://www.kikar.co.il/news"
    for link in kikar_link_list:
        if link and kikar_artc_word in link:
            kikar_clean_list.append(link)
    #del kikar_clean_list[-2:-1]

    for link in kikar_clean_list:
        if link and kikar_starter not in link:
            #link = kikar_starter + link
            kikar_clean_list_2.append(link)

    return kikar_clean_list_2
#print(get_kikar_links())


def get_nrg_links():
    
    nrg_link_list = []
    nrg_clean_list = []
    nrg_clean_list_2 = []

    with urllib.request.urlopen("http://www.nrg.co.il/online/HP_1.html") as url:
        s = url.read()

    soup = BeautifulSoup(s, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        nrg_link_list.append(href)

    #print(soup.prettify())


    nrg_artc_word = "/online/1/ART2"
    nrg_starter = "http://www.nrg.co.il"
    for link in nrg_link_list:
        if link and nrg_artc_word in link:
            nrg_clean_list.append(link)
    #del nrg_clean_list[-2:-1]

    for link in nrg_clean_list:
        if link and nrg_starter not in link:
            link = nrg_starter + link
            nrg_clean_list_2.append(link)

    return nrg_clean_list_2
#print(get_nrg_links())

def get_kan_links():
    
    kan_link_list = []
    kan_clean_list = []
    kan_clean_list_2 = []

    req = Request('http://www.kan.org.il/page.aspx?landingPageId=1009', headers={'User-Agent': 'Mozilla/5.0'})
    s = urlopen(req).read()

    soup = BeautifulSoup(s, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        kan_link_list.append(href)

    kan_artc_word = "/item"
    kan_starter = "http://www.kan.org.il"
    for link in kan_link_list:
        if link and kan_artc_word in link:
            kan_clean_list.append(link)

    for link in kan_clean_list:
        if link and kan_starter not in link:
            link = kan_starter + link
            kan_clean_list_2.append(link)

    return kan_clean_list_2
#print(get_kan_links())

#remove duplicate function
def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        # If value has not been encountered yet,
        # ... add it to both list and set.
        if value not in seen:
            output.append(value)
            seen.add(value)
            
    return output


def collect_lists():
    start_time = time.time()
    collecting_date = time.strftime("%D:%M:%Y")
    collecting_time = time.strftime("%H:%M:%S")

    global kikar_links_list,maariv_links_list,calcal_links_list,ynet_links_list,israel_ha_links_list,mako_links_list,walla_links_list,kan_links_list

    #nrg_links_list = remove_duplicates(get_nrg_links()) doesnt workkk
    kikar_links_list = remove_duplicates(get_kikar_links())
    print("kikar got links")
    maariv_links_list = remove_duplicates(get_maariv_links())
    print("maariv  got links")
    calcal_links_list = remove_duplicates(get_calcal_links())
    print("calcal  got links")
    ynet_links_list = remove_duplicates(get_ynet_links())
    print("ynet  got links",ynet_links_list)
    israel_ha_links_list = remove_duplicates(get_israel_ha_links())
    print("israel_ha got links")
    mako_links_list = remove_duplicates(get_mako_links())
    print("mako  got links")
    walla_links_list = remove_duplicates(get_walla_links())
    print("walla  got links")
    kan_links_list = remove_duplicates(get_kan_links())
    print("kan got links")

    #remove duplicate links:
    

    #print(walla_links_list,mako_links_list,ynet_links_list)

    end_time = time.time()
    time_taken = end_time - start_time
    #print("it took ",time_taken,"seconds to collect it")
    
    return(collecting_date,collecting_time)



"""

The End Of the links collection
Start of the scaning functions

"""


#Libary functions

def scan_kan(link):
    global artc
    
    page = requests.get(link)
    tree = html.fromstring(page.content)
    div = []
    p = tree.xpath('//p/text()')
    #print(p)
    text = ""
    for i in p:
        text += i
    artc = text
    artc = artc.encode('latin1').decode('utf8')
    return artc
#scan_kan("http://www.kan.org.il/item/?itemId=25344")


def scan_ynet(link):
    global artc
    
    page = requests.get(link)
    tree = html.fromstring(page.content)

    p = tree.xpath('//p/text()')
    text = ""
    for i in p:
        text += i
    artc = text
    return(artc)
 
#scan_ynet("http://www.ynet.co.il/articles/0,7340,L-4987816,00.html")

def scan_mako(link):
    global artc
    
    page = requests.get(link)
    tree = html.fromstring(page.content)

    p = tree.xpath('//p/text()')
    text = ""
    for i in p:
        text += i
    artc = text
    return(artc)

def scan_kikar(link):
    global artc
    
    page = requests.get(link)
    tree = html.fromstring(page.content)

    p = tree.xpath('//p/text()')
    text = ""
    for i in p:
        text += i
    artc = text
    print(artc)
    return(artc)

def scan_is_hayom(link):
    global artc
    
    page = requests.get(link)
    tree = html.fromstring(page.content)

    p = tree.xpath('//div/text()')
    del p[-72:]
    text = ""
    for i in p:
        text += i
    artc = text
    return(artc)

def scan_walla(link):
    global artc
    
    page = requests.get(link)
    tree = html.fromstring(page.content)

    p = tree.xpath('//p/text()')
    text = ""
    for i in p:
        text += i
    artc = text
    artc = artc.encode('latin1').decode('utf8')
    return(artc)
#scan_walla("https://news.walla.co.il/item/3107643")

def scan_maariv(link): #problematik - the text shows in strange letters
    global artc
    
    page = requests.get(link)
    tree = html.fromstring(page.content)

    p = tree.xpath('//div[@class="article-text"]/text()')
    text = ""
    for i in p:
        text += i
    artc = text
    artc = artc.encode('latin1').decode('utf8')
    return(artc)
#scan_maariv("http://www.maariv.co.il/news/viral/Article-605870")

def scan_globes(link): #problematik - the text shows in strange letters
    global artc
    
    page = requests.get(link)
    tree = html.fromstring(page.content)

    p = tree.xpath('//p/text()')
    text = ""
    for i in p:
        text += i
    artc = text
    return(artc)

#scan_globes("https://www.globes.co.il/news/article.aspx?did=1001209925")



"""

Anlyze

"""


def anlyz_artc(artc):
    
    def sort_un_words():
        #tokenize the article
        tokens_first = nltk.word_tokenize(artc) #nltk library func
        #here we're pull out the annoying parts
        list_unwanted_words = [" ","{","}","!","&","*","(",")","#","%","&","@","_","-","'"," \u2013","'s",'``','.',"''",'--',"--",",",")"," ,","("," ," , "." , "!" , "?" , "..." , ".." , "?!" , ":)" , ":" , "-" , "/" , "*" , ";" , ",","$"]

        tokens = []
        
        for word in tokens_first:
            word = word.lower()
            if word not in list_unwanted_words:
                tokens.append(word)
            
        #print(tokens)
        return tokens #we're returning a nice words list the made from the article
    artc_words = sort_un_words() #instead of call the "sort_un_words()" twice


    
    #in the two func() below we're compare the words from the article with the negative/positive words 
    
    def nagative_match():
        print("nega")
        global artc_len
        global nega_count
        nega_count = 0
        artc_len = len(artc_words)
        
        for word in artc_words:
            for i in list_negative:
                if i == word:
                    #print(i)
                    nega_count += 1

    def positive_match():
        print("posi")
        global artc_len
        global posi_count
        posi_count = 0
        artc_len = len(artc_words)
        for word in artc_words:
            for i in list_positive:
                if i == word:
                    #print(i)
                    posi_count += 1

    #here we do little (little) bit math...
                    
    def ratio():
        
        
        positive_match()   
        nagative_match()

        if artc_len != 0:
          
            posi_ratio = float(posi_count) / artc_len
            posi_pre_ratio = (float(posi_count) * 100) / artc_len
            nega_ratio = float(nega_count) / artc_len
            print("negative_ratio" , nega_ratio)
            print("positive_ratio" , posi_ratio)
            print("positive_ratio" , posi_pre_ratio, "%")
            #print("negative : positive", float(nega_count) / posi_count)
        else:
            posi_ratio,nega_ratio = None,None

        return(nega_ratio, posi_ratio)

    nega_ratio,posi_ratio = ratio()
    
    return(artc_len,posi_count,nega_count,nega_ratio, posi_ratio)



"""
Scans again and again

"""



def multi_links():
    collecting_date,collecting_time = collect_lists()

    sql_artc_data_list = []

    for link in israel_ha_links_list:
        source = "israel_hayom"
        print("\n\n another article ",source)
        artc = scan_is_hayom(link)
        print(artc)
        artc_len,posi_count,nega_count,nega_ratio, posi_ratio = anlyz_artc(artc)
        artc_row = [artc, link,source,None,collecting_date,collecting_time,artc_len,posi_count,nega_count,nega_ratio, posi_ratio]
        collecting_date += ""
        collecting_time += ""
        artc_len = str(artc_len)
        posi_count = str(posi_count)
        nega_count = str(nega_count)
        nega_ratio = str(nega_ratio)
        posi_ratio = str(posi_ratio)
        
        a = 'INSERT INTO artc VALUES (' + "'"  + link + "','"+source + "','" + collecting_date+ "','" +collecting_time + "','" + artc_len + "','" + nega_count+ "','" + posi_count+ "','" + nega_ratio+ "','" +  posi_ratio + "')"
        print(a)
        if int(artc_len) > 20:
            sql_artc_data_list.append(a)

    for link in kan_links_list:
        source = "Kan News"
        print("\n\n another article ",source)
        artc = scan_kan(link)
        
        artc_len,posi_count,nega_count,nega_ratio, posi_ratio = anlyz_artc(artc)
        artc_row = [artc, link,source,None,collecting_date,collecting_time,artc_len,posi_count,nega_count,nega_ratio, posi_ratio]
        collecting_date += ""
        collecting_time += ""
        artc_len = str(artc_len)
        posi_count = str(posi_count)
        nega_count = str(nega_count)
        nega_ratio = str(nega_ratio)
        posi_ratio = str(posi_ratio)
        
        a = 'INSERT INTO artc VALUES (' + "'"  + link + "','"+source + "','" + collecting_date+ "','" +collecting_time + "','" + artc_len + "','" + nega_count+ "','" + posi_count+ "','" + nega_ratio+ "','" +  posi_ratio + "')"
        print(a)
        if int(artc_len) > 20:
            sql_artc_data_list.append(a)


    
            
    for link in walla_links_list:
        source = "walla"
        print("\n\n another article ",source)
        artc = scan_walla(link)
        
        artc_len,posi_count,nega_count,nega_ratio, posi_ratio = anlyz_artc(artc)
        artc_row = [artc, link,source,None,collecting_date,collecting_time,artc_len,posi_count,nega_count,nega_ratio, posi_ratio]
        collecting_date += ""
        collecting_time += ""
        artc_len = str(artc_len)
        posi_count = str(posi_count)
        nega_count = str(nega_count)
        nega_ratio = str(nega_ratio)
        posi_ratio = str(posi_ratio)
        
        a = 'INSERT INTO artc VALUES (' + "'"  + link + "','"+source + "','" + collecting_date+ "','" +collecting_time + "','" + artc_len + "','" + nega_count+ "','" + posi_count+ "','" + nega_ratio+ "','" +  posi_ratio + "')"
        #print(a)
        if int(artc_len) > 20:
            sql_artc_data_list.append(a)
    
    for link in ynet_links_list:
        source = "ynet"
            
        #print(link)
        print("\n\n another article ",source)
        artc = scan_ynet(link)
        artc_len,posi_count,nega_count,nega_ratio, posi_ratio = anlyz_artc(artc)
        artc_row = [artc, link,source,None,collecting_date,collecting_time,artc_len,posi_count,nega_count,nega_ratio, posi_ratio]
        collecting_date += ""
        collecting_time += ""
        artc_len = str(artc_len)
        posi_count = str(posi_count)
        nega_count = str(nega_count)
        nega_ratio = str(nega_ratio)
        posi_ratio = str(posi_ratio)
        
        a = 'INSERT INTO artc VALUES (' + "'"  + link + "','"+source + "','" + collecting_date+ "','" +collecting_time + "','" + artc_len + "','" + nega_count+ "','" + posi_count+ "','" + nega_ratio+ "','" +  posi_ratio + "')"
        #print(a)
        if int(artc_len) > 20:
            sql_artc_data_list.append(a)

        
    for link in mako_links_list:
        source = "mako"
        print("\n\n another article ",source)
        artc = scan_mako(link)
        
        artc_len,posi_count,nega_count,nega_ratio, posi_ratio = anlyz_artc(artc)
        artc_row = [artc, link,source,None,collecting_date,collecting_time,artc_len,posi_count,nega_count,nega_ratio, posi_ratio]
        collecting_date += ""
        collecting_time += ""
        artc_len = str(artc_len)
        posi_count = str(posi_count)
        nega_count = str(nega_count)
        nega_ratio = str(nega_ratio)
        posi_ratio = str(posi_ratio)
        
        a = 'INSERT INTO artc VALUES (' + "'"  + link + "','"+source + "','" + collecting_date+ "','" +collecting_time + "','" + artc_len + "','" + nega_count+ "','" + posi_count+ "','" + nega_ratio+ "','" +  posi_ratio + "')"
        if int(artc_len) > 20:
            sql_artc_data_list.append(a)
        

    for link in calcal_links_list:
        source = "calcalist"
        print("\n\n another article ",source)
        artc = scan_ynet(link)
        
        artc_len,posi_count,nega_count,nega_ratio, posi_ratio = anlyz_artc(artc)
        artc_row = [artc, link,source,None,collecting_date,collecting_time,artc_len,posi_count,nega_count,nega_ratio, posi_ratio]
        collecting_date += ""
        collecting_time += ""
        artc_len = str(artc_len)
        posi_count = str(posi_count)
        nega_count = str(nega_count)
        nega_ratio = str(nega_ratio)
        posi_ratio = str(posi_ratio)
        
        a = 'INSERT INTO artc VALUES (' + "'"  + link + "','"+source + "','" + collecting_date+ "','" +collecting_time + "','" + artc_len + "','" + nega_count+ "','" + posi_count+ "','" + nega_ratio+ "','" +  posi_ratio + "')"
        #print(a)
        if int(artc_len) > 20:
            sql_artc_data_list.append(a)

    print("\n\n\n\nDone!")

            
    return( sql_artc_data_list)

       
    
        
#multi_links()




if write_sql == True:

    #
    start_time = time.time()
    #
    
    #Connect to the DB
    conn = sql.connect('db_try_1.sqlite3')

    c = conn.cursor()

    sql_artc_data_list = multi_links()
    for a in sql_artc_data_list:
        c.execute(a)
    conn.commit()
    conn.close()

    #
    end_time = time.time()
    time_taken = end_time - start_time
    print("it took ",time_taken,"seconds to collect it")
    #

#To do:
        #fix the positive_list in the anlyz_hebrew_2 file

"""
Scan probs:

globes
maariv


Scrap probs:

kikar
nrg


Workig:
mako
walla
ynet
israel ha
kan
"""





"""
#nrg_links_list = get_nrg_links() doesnt workkk
    kikar_links_list = get_kikar_links()
    maariv_links_list = get_maariv_links()
    calcal_links_list = get_calcal_links()
    ynet_links_list = get_ynet_links()
    israel_ha_links_list = get_israel_ha_links()
    mako_links_list = get_mako_links()
    walla_links_list = get_walla_links()
"""
"""
#Test area:
ynet_links_list = remove_duplicates(get_ynet_links())
print("ynet  got links",ynet_links_list)
"""






