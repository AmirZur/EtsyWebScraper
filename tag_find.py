import urllib
from bs4 import BeautifulSoup
import re

base_url = "https://www.etsy.com/search?q="
taglist = list()

taglist_file = open("tag_list.txt")
for line in taglist_file:
  line = line.strip()
  taglist.append(line)

taglist1 = ["black friday", "black friday sale", "gold stud earrings"]

tracksheet = open("tracksheet.txt", "w")
  
url = ""  
for tag in taglist1:
  tag = tag.split()
  url = base_url + "+".join(tag)      
      
  html = urllib.urlopen(url).read()
  soup = BeautifulSoup(html, "html.parser")
  
  resultstag = soup.find("div", {"class":"clearfix pb-xs-1-5"}).div.div.contents[-2]
  results = resultstag.string
  results_number = re.findall("[0-9,]+", results)[0]
  
  mtcount = 0
  pwcount = 0 
  isintitlelist_mt = []
  isintitlelist_pw = []
  tagword = " ".join(tag)
  nextpage = url
  for page in range(3):
    html = urllib.urlopen(nextpage).read()
    soup = BeautifulSoup(html, "html.parser")
    
    store_tags = soup(attrs="card-shop-name")   
    stores = list()
    
    for store_tag in store_tags:
      store = store_tag.string.strip()
      if store == "MtCarmelJewelry":
        title_tag = store_tag.parent.parent.div.div
        title = str(title_tag.string.strip()).lower()
        isintitle = bool(str(tagword) in title)
        isintitlelist_mt.append(isintitle)
        mtcount += 1
      elif store == "ThePostwoman":
        title_tag = store_tag.parent.parent.div.div
        title = str(title_tag.string.strip()).lower()
        isintitle = bool(str(tagword) in title)        
        isintitlelist_pw.append(isintitle)
        pwcount += 1
    
    nextpage = url + "&explicit=1&page=" + str(page+1)
  
  intitles_mt = filter(lambda x: x == True, isintitlelist_mt)
  intitles_pw = filter(lambda x: x == True, isintitlelist_pw)
  
  
  final_list = [str(" ".join(tag)), results_number, str(mtcount), str(len(intitles_mt)), str(pwcount), str(len(intitles_pw))]
  #In order: Search, number of all results, number of Mt. Carmel Jewelry, number with search in title, number of Post Woman, number with search in title 
  tracksheet.write(" ".join(final_list) + "\n")
  
  #In order: Search, number of all results, number of Mt. Carmel Jewelry, number with search in title, number of Post Woman, number with search in title 
  print " ".join(final_list)
  print ""

tracksheet.close() 
  
  