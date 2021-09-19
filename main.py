from concurrent.futures import ThreadPoolExecutor
import requests
import wget
import os
from bs4 import BeautifulSoup as bsp

executor = ThreadPoolExecutor(max_workers=8)

def fetchURL(url):
    print("Fetching %s"%(url))
    t = requests.get(url).text
    return t

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

def getPapers(link):
    ppr = None
    newAddr = "https://openai.com" + link
    html = requests.get(newAddr).text
    newBowl = bsp(html, features="html.parser").find_all('a')
    for link in newBowl:
        newlink = link.get("href")
        if newlink is not None and "arxiv" in newlink:
            if os.path.exists("saved"):
                executor.submit(downloadPaper, newlink)
            else:
                os.mkdir("saved")
                executor.submit(downloadPaper, newlink)
            

#define the root page
topAddr = "https://openai.com/blog/tags/milestones/"
html = fetchURL(topAddr)
soupBowl = bsp(html, features="html.parser")

blog = soupBowl.find_all('a')
leadHolder = []
for link in blog:
    newlink = link.get("href")
    if "blog" in newlink:
        leadHolder.append(newlink)

for link in leadHolder:
    getPapers(link)

executor.shutdown(wait=True)