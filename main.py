from concurrent.futures import ThreadPoolExecutor
import requests
import wget
import os
from bs4 import BeautifulSoup as bsp

executor = ThreadPoolExecutor(max_workers=32)

mainURL = "https://arxiv.org"

targetList = open("targets.txt", "r").readlines()

#make a url for the purposes of downloading a pdf
def makeURL(baseSite:str, urlStub:str) -> str:
    return baseSite + urlStub

def openPage(url:str) -> str:
    return requests.get(url).text

def getPDFLinks(page:str) -> list:
    soup = bsp(page, "html.parser")
    pdfLink = soup.findAll("a", {"title":"Download PDF"})
    holder = []
    for link in pdfLink:
        holder.append(link["href"])
    return holder

def sanitizeTarget(target:str) -> str:
    target = target.replace("https://", "")
    target = target.replace("/", "")
    target = target.replace(":", "")
    target = target.replace(" ", "")
    return target

def downloadSingleFile(pdfLink:str, target:str):
    print("Downloading PDF: ", pdfLink)
    if pdfLink:
        sanitizedTarget = sanitizeTarget(target)
        pdfURL = makeURL(mainURL, pdfLink)
        pdfName = pdfLink.split("/")[-1]
        sanitizedPDFName = sanitizeTarget(pdfName)
        print(f"Downloading {pdfName} for {target}")
        #if the folder structure doesn't exist, create it
        if not os.path.exists(f"pdfs/{sanitizedTarget}"):
            os.makedirs(f"pdfs/{sanitizedTarget}")
        #if the file does not already exist, download it
        if not os.path.exists(f"pdfs/{sanitizedTarget}/{sanitizedPDFName}.pdf"):
            print(f"Downloading {pdfName} for {target}")
            wget.download(pdfURL, out=f"pdfs/{sanitizedTarget}/{sanitizedPDFName}.pdf")
        else:
            print(f"Could not find PDF for {target}")

def downloadPDFs(url:str, target:str):
    pdfLinks = getPDFLinks(openPage(target))
    for pdfLink in pdfLinks:
        print("Attempting to download PDF: ", pdfLink)
        executor.submit(downloadSingleFile, pdfLink, url)

def doAllDownloads():
    print("Starting downloads...")
    print("Targets: ", targetList)
    for target in targetList:
        target = target.strip()
        downloadPDFs(mainURL, target)

doAllDownloads()

executor.shutdown(wait=True)

print("All PDFs downloaded!")