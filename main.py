import requests
import wget
import os
from bs4 import BeautifulSoup as bsp

#define the root page
topAddr = "https://openai.com/blog/tags/milestones/"
html = requests.get(topAddr).text
soupBowl = bsp(html)

blog = soupBowl.find_all('a')
leadHolder = []
for link in blog:
    newlink = link.get("href")
    if "blog" in newlink:
        leadHolder.append(newlink)

papers=[]
for link in leadHolder:
    newAddr = "https://openai.com" + link
    html = requests.get(newAddr).text
    newBowl = bsp(html).find_all('a')
    for link in newBowl:
        newlink = link.get("href")
        if newlink is not None and "arxiv" in newlink:
            papers.append(newlink)

if os.path.exists("saved"):
    if os.path.isdir("saved"):
        print("--saved directory exists--")
    else:
        os.mkdir("saved")
else:
    os.mkdir("saved")

def downloadPaper(url):
    urlobj = url.split("/")
    urlobj[3] = "pdf"
    urlobj[-1] += ".pdf"
    newUrl = ""
    for item in urlobj:
        newUrl += item + "/"
    newUrl = newUrl[:-1]
    filename = "saved/" + urlobj[-1]
    print("Downloading %s"%(newUrl))
    if not os.path.exists(filename):
        wget.download(newUrl, filename)
    else:
        print("%s already exists"%(filename))

for link in papers:
    downloadPaper(link)
    print("Ok we're done here.")
